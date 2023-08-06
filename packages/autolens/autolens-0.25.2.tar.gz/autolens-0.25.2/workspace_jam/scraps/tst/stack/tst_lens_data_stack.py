import numpy as np
import pytest

from autolens.data import ccd as im, convolution
from autolens.data.array.util import grid_util
from autolens.data.array import scaled_array
from autolens.data.array import mask as msk
from workspace_jam.scraps.stack import lens_data_stack as lis
from autolens.model.inversion import convolution as inversion_convolution


@pytest.fixture(name="ccd_0")
def make_image_0():

    image = scaled_array.ScaledSquarePixelArray(array=np.ones((4, 4)), pixel_scale=3.0)
    psf = im.PSF(array=np.ones((3, 3)), pixel_scale=3.0, renormalize=False)
    noise_map = im.NoiseMap(array=2.0 * np.ones((4, 4)), pixel_scale=3.0)
    background_noise_map = im.NoiseMap(array=3.0 * np.ones((4, 4)), pixel_scale=3.0)
    poisson_noise_map = im.PoissonNoiseMap(array=4.0 * np.ones((4, 4)), pixel_scale=3.0)
    exposure_time_map = im.ExposureTimeMap(array=5.0 * np.ones((4, 4)), pixel_scale=3.0)
    background_sky_map = scaled_array.ScaledSquarePixelArray(
        array=6.0 * np.ones((4, 4)), pixel_scale=3.0
    )

    return im.CCDData(
        image=image,
        pixel_scale=3.0,
        psf=psf,
        noise_map=noise_map,
        background_noise_map=background_noise_map,
        poisson_noise_map=poisson_noise_map,
        exposure_time_map=exposure_time_map,
        background_sky_map=background_sky_map,
    )


@pytest.fixture(name="ccd_1")
def make_image_1():

    image = scaled_array.ScaledSquarePixelArray(
        array=10.0 * np.ones((4, 4)), pixel_scale=6.0
    )
    psf = im.PSF(array=11.0 * np.ones((3, 3)), pixel_scale=6.0, renormalize=False)
    noise_map = im.NoiseMap(array=12.0 * np.ones((4, 4)), pixel_scale=6.0)
    background_noise_map = im.NoiseMap(array=13.0 * np.ones((4, 4)), pixel_scale=6.0)
    poisson_noise_map = im.PoissonNoiseMap(
        array=14.0 * np.ones((4, 4)), pixel_scale=6.0
    )
    exposure_time_map = im.ExposureTimeMap(
        array=15.0 * np.ones((4, 4)), pixel_scale=6.0
    )
    background_sky_map = scaled_array.ScaledSquarePixelArray(
        array=16.0 * np.ones((4, 4)), pixel_scale=6.0
    )

    return im.CCDData(
        image=image,
        pixel_scale=6.0,
        psf=psf,
        noise_map=noise_map,
        background_noise_map=background_noise_map,
        poisson_noise_map=poisson_noise_map,
        exposure_time_map=exposure_time_map,
        background_sky_map=background_sky_map,
    )


@pytest.fixture(name="mask_0")
def make_mask_0():
    return msk.Mask(
        np.array(
            [
                [True, True, True, True],
                [True, False, False, True],
                [True, False, False, True],
                [True, True, True, True],
            ]
        ),
        pixel_scale=3.0,
    )


@pytest.fixture(name="mask_1")
def make_mask_1():
    return msk.Mask(
        np.array(
            [
                [True, True, True, True],
                [True, False, False, True],
                [True, False, False, True],
                [True, True, True, True],
            ]
        ),
        pixel_scale=6.0,
    )


@pytest.fixture(name="lens_data_stack")
def make_lens_image(ccd_0, ccd_1, mask_0, mask_1):
    return lis.LensDataStack(ccd_datas=[ccd_0, ccd_1], masks=[mask_0, mask_1])


class TestLensData(object):
    def test_attributes(self, ccd_0, ccd_1, lens_data_stack):

        assert lens_data_stack.pixel_scales[0] == ccd_0.pixel_scale
        assert lens_data_stack.pixel_scales[0] == 3.0
        assert (lens_data_stack.images[0] == ccd_0.image).all()
        assert (lens_data_stack.images[0] == np.ones((4, 4))).all()
        assert (lens_data_stack.psfs[0] == ccd_0.psf).all()
        assert (lens_data_stack.psfs[0] == np.ones((3, 3))).all()
        assert (lens_data_stack.noise_maps[0] == ccd_0.noise_map).all()
        assert (lens_data_stack.noise_maps[0] == 2.0 * np.ones((4, 4))).all()

        assert lens_data_stack.pixel_scales[1] == ccd_1.pixel_scale
        assert lens_data_stack.pixel_scales[1] == 6.0
        assert (lens_data_stack.images[1] == ccd_1.image).all()
        assert (lens_data_stack.images[1] == 10.0 * np.ones((4, 4))).all()
        assert (lens_data_stack.psfs[1] == ccd_1.psf).all()
        assert (lens_data_stack.psfs[1] == 11.0 * np.ones((3, 3))).all()
        assert (lens_data_stack.noise_maps[1] == ccd_1.noise_map).all()
        assert (lens_data_stack.noise_maps[1] == 12.0 * np.ones((4, 4))).all()

    def test_masking(self, lens_data_stack):

        assert (lens_data_stack.images_1d[0] == np.ones(4)).all()
        assert (lens_data_stack.noise_maps_1d[0] == 2.0 * np.ones(4)).all()
        assert (
            lens_data_stack.masks_1d[0] == np.array([False, False, False, False])
        ).all()

        assert (lens_data_stack.images_1d[1] == 10.0 * np.ones(4)).all()
        assert (lens_data_stack.noise_maps_1d[1] == 12.0 * np.ones(4)).all()
        assert (
            lens_data_stack.masks_1d[1] == np.array([False, False, False, False])
        ).all()

    def test_grids(self, lens_data_stack):

        assert (
            lens_data_stack.grid_stacks[0].regular
            == np.array([[1.5, -1.5], [1.5, 1.5], [-1.5, -1.5], [-1.5, 1.5]])
        ).all()

        assert (
            lens_data_stack.grid_stacks[0].sub
            == np.array(
                [
                    [2.0, -2.0],
                    [2.0, -1.0],
                    [1.0, -2.0],
                    [1.0, -1.0],
                    [2.0, 1.0],
                    [2.0, 2.0],
                    [1.0, 1.0],
                    [1.0, 2.0],
                    [-1.0, -2.0],
                    [-1.0, -1.0],
                    [-2.0, -2.0],
                    [-2.0, -1.0],
                    [-1.0, 1.0],
                    [-1.0, 2.0],
                    [-2.0, 1.0],
                    [-2.0, 2.0],
                ]
            )
        ).all()

        assert (
            lens_data_stack.grid_stacks[0].blurring
            == np.array(
                [
                    [4.5, -4.5],
                    [4.5, -1.5],
                    [4.5, 1.5],
                    [4.5, 4.5],
                    [1.5, -4.5],
                    [1.5, 4.5],
                    [-1.5, -4.5],
                    [-1.5, 4.5],
                    [-4.5, -4.5],
                    [-4.5, -1.5],
                    [-4.5, 1.5],
                    [-4.5, 4.5],
                ]
            )
        ).all()

        # Pixel scale is doubled, thus the grids of coordinates are doubled.

        assert (
            lens_data_stack.grid_stacks[1].regular
            == 2.0 * np.array([[1.5, -1.5], [1.5, 1.5], [-1.5, -1.5], [-1.5, 1.5]])
        ).all()

        assert (
            lens_data_stack.grid_stacks[1].sub
            == 2.0
            * np.array(
                [
                    [2.0, -2.0],
                    [2.0, -1.0],
                    [1.0, -2.0],
                    [1.0, -1.0],
                    [2.0, 1.0],
                    [2.0, 2.0],
                    [1.0, 1.0],
                    [1.0, 2.0],
                    [-1.0, -2.0],
                    [-1.0, -1.0],
                    [-2.0, -2.0],
                    [-2.0, -1.0],
                    [-1.0, 1.0],
                    [-1.0, 2.0],
                    [-2.0, 1.0],
                    [-2.0, 2.0],
                ]
            )
        ).all()

        assert (
            lens_data_stack.grid_stacks[1].blurring
            == 2.0
            * np.array(
                [
                    [4.5, -4.5],
                    [4.5, -1.5],
                    [4.5, 1.5],
                    [4.5, 4.5],
                    [1.5, -4.5],
                    [1.5, 4.5],
                    [-1.5, -4.5],
                    [-1.5, 4.5],
                    [-4.5, -4.5],
                    [-4.5, -1.5],
                    [-4.5, 1.5],
                    [-4.5, 4.5],
                ]
            )
        ).all()

    def test_padded_grid_stack(self, lens_data_stack):

        padded_image_util = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(
            mask=np.full((6, 6), False),
            pixel_scales=lens_data_stack.images[0].pixel_scales,
        )

        assert (
            lens_data_stack.padded_grid_stacks[0].regular == padded_image_util
        ).all()
        assert lens_data_stack.padded_grid_stacks[0].regular.image_shape == (4, 4)
        assert lens_data_stack.padded_grid_stacks[0].regular.padded_shape == (6, 6)

        padded_sub_util = grid_util.sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size_non_optimal_spacing(
            mask=np.full((6, 6), False),
            pixel_scales=lens_data_stack.images[0].pixel_scales,
            sub_grid_size=lens_data_stack.grid_stacks[0].sub.sub_grid_size,
        )

        assert lens_data_stack.padded_grid_stacks[0].sub == pytest.approx(
            padded_sub_util, 1e-4
        )
        assert lens_data_stack.padded_grid_stacks[0].sub.image_shape == (4, 4)
        assert lens_data_stack.padded_grid_stacks[0].sub.padded_shape == (6, 6)
        assert (
            lens_data_stack.padded_grid_stacks[0].blurring == np.array([[0.0, 0.0]])
        ).all()

        padded_image_util = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(
            mask=np.full((6, 6), False),
            pixel_scales=lens_data_stack.images[1].pixel_scales,
        )

        assert (
            lens_data_stack.padded_grid_stacks[1].regular == padded_image_util
        ).all()
        assert lens_data_stack.padded_grid_stacks[1].regular.image_shape == (4, 4)
        assert lens_data_stack.padded_grid_stacks[1].regular.padded_shape == (6, 6)

        padded_sub_util = grid_util.sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size_non_optimal_spacing(
            mask=np.full((6, 6), False),
            pixel_scales=lens_data_stack.images[1].pixel_scales,
            sub_grid_size=lens_data_stack.grid_stacks[1].sub.sub_grid_size,
        )

        assert lens_data_stack.padded_grid_stacks[1].sub == pytest.approx(
            padded_sub_util, 1e-4
        )
        assert lens_data_stack.padded_grid_stacks[1].sub.image_shape == (4, 4)
        assert lens_data_stack.padded_grid_stacks[1].sub.padded_shape == (6, 6)
        assert (
            lens_data_stack.padded_grid_stacks[1].blurring == np.array([[0.0, 0.0]])
        ).all()

        # Pixel scale is doubled, thus the grids of coordinates are doubled.

        assert (
            2.0 * lens_data_stack.padded_grid_stacks[0].regular
            == lens_data_stack.padded_grid_stacks[1].regular
        ).all()
        assert (
            2.0 * lens_data_stack.padded_grid_stacks[0].sub
            == lens_data_stack.padded_grid_stacks[1].sub
        ).all()

    def test_border(self, lens_data_stack):
        assert (lens_data_stack.borders[0] == np.array([0, 1, 2, 3])).all()
        assert (lens_data_stack.borders[1] == np.array([0, 1, 2, 3])).all()

    def test_convolvers(self, lens_data_stack):
        assert type(lens_data_stack.convolvers_image[0]) == convolution.ConvolverImage
        assert (
            type(lens_data_stack.convolvers_mapping_matrix[0])
            == inversion_convolution.ConvolverMappingMatrix
        )
        assert type(lens_data_stack.convolvers_image[1]) == convolution.ConvolverImage
        assert (
            type(lens_data_stack.convolvers_mapping_matrix[1])
            == inversion_convolution.ConvolverMappingMatrix
        )

    def test__constructor_inputs(self):

        psf_0 = im.PSF(np.ones((7, 7)), 1)
        ccd_0 = im.CCDData(
            np.ones((51, 51)), pixel_scale=3.0, psf=psf_0, noise_map=np.ones((51, 51))
        )
        mask_0 = msk.Mask.unmasked_for_shape_and_pixel_scale(
            shape=(51, 51), pixel_scale=1.0, invert=True
        )
        mask_0[26, 26] = False

        psf_1 = im.PSF(np.ones((7, 7)), 1)
        ccd_1 = im.CCDData(
            np.ones((51, 51)), pixel_scale=3.0, psf=psf_1, noise_map=np.ones((51, 51))
        )
        mask_1 = msk.Mask.unmasked_for_shape_and_pixel_scale(
            shape=(51, 51), pixel_scale=1.0, invert=True
        )
        mask_1[26, 26] = False

        lens_data_stack = lis.LensDataStack(
            ccd_datas=[ccd_0, ccd_1],
            masks=[mask_0, mask_1],
            sub_grid_size=8,
            image_psf_shape=(5, 5),
            mapping_matrix_psf_shape=(3, 3),
            positions=[np.array([[1.0, 1.0]])],
        )

        assert lens_data_stack.sub_grid_size == 8
        assert lens_data_stack.convolvers_image[0].psf_shape == (5, 5)
        assert lens_data_stack.convolvers_mapping_matrix[0].psf_shape == (3, 3)
        assert lens_data_stack.convolvers_image[1].psf_shape == (5, 5)
        assert lens_data_stack.convolvers_mapping_matrix[1].psf_shape == (3, 3)
        assert (lens_data_stack.positions[0] == np.array([[1.0, 1.0]])).all()


@pytest.fixture(name="lens_hyper_image_stack")
def make_lens_hyper_image(ccd_0, ccd_1, mask_0, mask_1):

    return lis.LensHyperDataStack(
        ccd_datas=[ccd_0, ccd_1],
        masks=[mask_0, mask_1],
        hyper_model_images=[10.0 * np.ones((4, 4)), 20.0 * np.ones((4, 4))],
        hyper_galaxy_images_stack=[
            [11.0 * np.ones((4, 4)), 12.0 * np.ones((4, 4))],
            [21.0 * np.ones((4, 4)), 22.0 * np.ones((4, 4))],
        ],
        hyper_minimum_values=[0.1, 0.2],
    )


class TestLensingHyperImage(object):
    def test_attributes(self, ccd_0, ccd_1, lens_hyper_image_stack):

        assert lens_hyper_image_stack.pixel_scales[0] == ccd_0.pixel_scale

        assert (lens_hyper_image_stack.images[0] == ccd_0.image).all()
        assert (lens_hyper_image_stack.images[0] == np.ones((4, 4))).all()

        assert (lens_hyper_image_stack.psfs[0] == ccd_0.psf).all()
        assert (lens_hyper_image_stack.psfs[0] == np.ones((3, 3))).all()

        assert (lens_hyper_image_stack.noise_maps[0] == ccd_0.noise_map).all()
        assert (lens_hyper_image_stack.noise_maps[0] == 2.0 * np.ones((4, 4))).all()

        assert (
            lens_hyper_image_stack.hyper_model_images[0] == 10.0 * np.ones((4, 4))
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_stack[0][0]
            == 11.0 * np.ones((4, 4))
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_stack[0][1]
            == 12.0 * np.ones((4, 4))
        ).all()

        assert lens_hyper_image_stack.pixel_scales[1] == ccd_1.pixel_scale

        assert (lens_hyper_image_stack.images[1] == ccd_1.image).all()
        assert (lens_hyper_image_stack.images[1] == 10.0 * np.ones((4, 4))).all()

        assert (lens_hyper_image_stack.psfs[1] == ccd_1.psf).all()
        assert (lens_hyper_image_stack.psfs[1] == 11.0 * np.ones((3, 3))).all()

        assert (lens_hyper_image_stack.noise_maps[1] == ccd_1.noise_map).all()
        assert (lens_hyper_image_stack.noise_maps[1] == 12.0 * np.ones((4, 4))).all()

        assert (
            lens_hyper_image_stack.hyper_model_images[1] == 20.0 * np.ones((4, 4))
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_stack[1][0]
            == 21.0 * np.ones((4, 4))
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_stack[1][1]
            == 22.0 * np.ones((4, 4))
        ).all()

        assert lens_hyper_image_stack.hyper_minimum_values == [0.1, 0.2]

    def test_masking(self, lens_hyper_image_stack):

        assert (lens_hyper_image_stack.images_1d[0] == np.ones(4)).all()
        assert (lens_hyper_image_stack.noise_maps_1d[0] == 2.0 * np.ones(4)).all()

        assert (
            lens_hyper_image_stack.hyper_model_images_1d[0] == 10.0 * np.ones(4)
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_1d_stack[0][0]
            == 11.0 * np.ones(4)
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_1d_stack[0][1]
            == 12.0 * np.ones(4)
        ).all()

        assert (lens_hyper_image_stack.images_1d[1] == 10.0 * np.ones(4)).all()
        assert (lens_hyper_image_stack.noise_maps_1d[1] == 12.0 * np.ones(4)).all()

        assert (
            lens_hyper_image_stack.hyper_model_images_1d[1] == 20.0 * np.ones(4)
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_1d_stack[1][0]
            == 21.0 * np.ones(4)
        ).all()
        assert (
            lens_hyper_image_stack.hyper_galaxy_images_1d_stack[1][1]
            == 22.0 * np.ones(4)
        ).all()
