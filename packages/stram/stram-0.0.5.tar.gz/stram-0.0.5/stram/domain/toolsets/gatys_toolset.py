import tensorflow as tf
import tensorflow.keras as keras
from static_variables import resolve_static


def gram_matrix(input_tensor):
    """
    Compute the gram matrix on the last dimension of the input tensor

    Args:
        input_tensor (tf.Tensor): tensor of rank 4
    Return:
        gram_matrix (tf.Tensor): tensor of rank 3
    """
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / num_locations


def _get_magnitude_normalisation_factors(power=1.0):
    """
    Get a dict with custom normalisation factors for each layer in the VGG19.
    The values have been computed by averaging the activations of the entire unlabelled
    dataset of COCO 2017 when passing the data through the network

    Args:
        power (float): exponent for base values based on further usage
    Return:
        normalisation_factors (dict): maps layer name to normalisation value
    """
    average_vgg19_layer_activation = dict(
        block1_conv1=21.3766174316406,
        block1_conv2=98.0979156494141,
        block2_conv1=123.892250061035,
        block2_conv2=111.009941101074,
        block3_conv1=127.140815734863,
        block3_conv2=164.742660522461,
        block3_conv3=345.452362060547,
        block3_conv4=509.229614257812,
        block4_conv1=526.813049316406,
        block4_conv2=346.448577880859,
        block4_conv3=193.982391357422,
        block4_conv4=47.8912048339844,
        block5_conv1=51.1512794494629,
        block5_conv2=21.5614013671875,
        block5_conv3=8.86503982543945,
        block5_conv4=1.11896836757660,
    )
    return {key: value ** power for key, value in average_vgg19_layer_activation.items()}


@resolve_static(
    static_variables={
        'mse': keras.losses.MeanSquaredError(),
        'normalisation_factors': _get_magnitude_normalisation_factors(2.0),
    }
)
def content_loss(content_features, synthesized_features, weights):
    """
    Compute the weighted mean squared error between two dictionaries of
    corresponding tensors

    Args:
        content_features (dict): maps layer name to extracted features
        synthesized_features (dict): maps layer name to extracted features
        weights (dict): maps layer name to corresponding loss weight
    Return:
        loss_value (tf.float32): the loss value
    """
    loss_value = 0.0
    for name, features in content_features.items():
        weight = weights[name] / normalisation_factors[name]
        loss_value += weight * mse(features, synthesized_features[name])

    return loss_value


@resolve_static(
    static_variables={
        'mse': keras.losses.MeanSquaredError(),
        'normalisation_factors': _get_magnitude_normalisation_factors(4.0),
    }
)
def style_loss(style_gram_matrices, synthesized_features, weights):
    """
    Compute the weighted mean squared error between two dictionaries of
    gram matrices from corresponding tensors

    Args:
        style_gram_matrices (dict): maps layer name to gram matrix
        synthesized_features (dict): maps layer name to extracted features
        weights (dict): maps layer name to corresponding loss weight
    Return:
        loss_value (tf.float32): the loss value
    """
    loss_value = 0.0
    for name, true_gm in style_gram_matrices.items():
        weight = weights[name] / normalisation_factors[name]
        gm = gram_matrix(synthesized_features[name])
        loss_value += weight * mse(true_gm, gm)

    return loss_value
