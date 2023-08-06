class Analysis(af.Analysis):
    def __init__(
        self, lens_data, hyper_model_image_1d, hyper_galaxy_image_1d_path_dict
    ):
        """
        An analysis to fit the noise for a single galaxy image.
        Parameters
        ----------
        lens_data: LensData
            Lens data, including an image and noise
        hyper_model_image_1d: ndarray
            An image produce of the overall system by a model
        hyper_galaxy_image_1d_path_dict: ndarray
            The contribution of one galaxy to the model image
        """

        self.lens_data = lens_data

        self.hyper_galaxy_image_1d_path_dict = hyper_galaxy_image_1d_path_dict

        self.hyper_model_image_1d = hyper_model_image_1d

        #    self.check_for_previously_masked_values(array=self.hyper_model_image_1d)
        #    self.check_for_previously_masked_values(array=self.hyper_galaxy_image_1d)

        self.plot_hyper_galaxy_subplot = af.conf.instance.visualize.get(
            "plots", "plot_hyper_galaxy_subplot", bool
        )

    @staticmethod
    def check_for_previously_masked_values(array):
        if not np.all(array) != 0.0:
            raise exc.PhaseException(
                "When mapping a 2D array to a 1D array using lens data, a value "
                "encountered was 0.0 and therefore masked in a previous phase."
            )

    def visualize(self, instance, image_path, during_analysis):

        if self.plot_hyper_galaxy_subplot:

            hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

            hyper_noise_background = self.hyper_noise_background_for_instance(
                instance=instance
            )

            hyper_model_image_2d = self.lens_data.scaled_array_2d_from_array_1d(
                array_1d=self.hyper_model_image_1d
            )

            for galaxy_path, galaxy in instance.path_instance_tuples_for_class(
                g.Galaxy
            ):

                if galaxy_path in self.hyper_galaxy_image_1d_path_dict:
                    hyper_galaxy_image_2d = self.lens_data.scaled_array_2d_from_array_1d(
                        array_1d=self.hyper_galaxy_image_1d_path_dict[galaxy_path]
                    )

                # contribution_map_2d = galaxy.hyper_galaxy.contribution_map_from_hyper_images(
                #     hyper_model_image=hyper_model_image_2d,
                #     hyper_galaxy_image=hyper_galaxy_image_2d,
                # )

                fit_normal = lens_fit.LensDataFit(
                    image_1d=self.lens_data.image_1d,
                    noise_map_1d=self.lens_data.noise_map_1d,
                    mask_1d=self.lens_data.mask_1d,
                    model_image_1d=self.hyper_model_image_1d,
                    grid_stack=self.lens_data.grid_stack,
                )

                fit = self.fit_for_hyper_galaxy(
                    instance=instance,
                    hyper_galaxy=galaxy.hyper_galaxy,
                    hyper_image_sky=hyper_image_sky,
                    hyper_noise_background=hyper_noise_background,
                )

                hyper_plotters.plot_hyper_galaxy_subplot(
                    hyper_galaxy_image=hyper_galaxy_image_2d,
                    contribution_map=contribution_map_2d,
                    noise_map=self.lens_data.noise_map(return_in_2d=True),
                    hyper_noise_map=fit.noise_map(return_in_2d=True),
                    chi_squared_map=fit_normal.chi_squared_map(return_in_2d=True),
                    hyper_chi_squared_map=fit.chi_squared_map(return_in_2d=True),
                    output_path=image_path,
                    output_format="png",
                )

    def fit(self, instance):
        """
        Fit the model image to the real image by scaling the hyper noise.
        Parameters
        ----------
        instance: ModelInstance
            A model instance with a hyper galaxy property
        Returns
        -------
        fit: float
        """

        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

        hyper_noise_background = self.hyper_noise_background_for_instance(
            instance=instance
        )

        fit = self.fit_for_hyper_galaxy(
            instance=instance,
            hyper_galaxy=instance.hyper_galaxy,
            hyper_image_sky=hyper_image_sky,
            hyper_noise_background=hyper_noise_background,
        )

        return fit.figure_of_merit

    @staticmethod
    def hyper_image_sky_for_instance(instance):
        if hasattr(instance, "hyper_image_sky"):
            return instance.hyper_image_sky

    @staticmethod
    def hyper_noise_background_for_instance(instance):
        if hasattr(instance, "hyper_noise_background"):
            return instance.hyper_noise_background

    def fit_for_hyper_galaxy(
        self, instance, hyper_galaxy, hyper_image_sky, hyper_noise_background
    ):

        if hyper_image_sky is not None:
            image_1d = hyper_image_sky.image_scaled_sky_from_image(
                image=self.lens_data.image_1d
            )
        else:
            image_1d = self.lens_data.image_1d

        if hyper_noise_background is not None:
            noise_map_1d = hyper_noise_background.noise_map_scaled_noise_from_noise_map(
                noise_map=self.lens_data.noise_map_1d
            )
        else:
            noise_map_1d = self.lens_data.noise_map_1d

        for galaxy_path, galaxy in instance.path_instance_tuples_for_class(g.Galaxy):

            hyper_noise_1d = np.zeros(shape=self.hyper_model_image_1d.shape)

            if galaxy_path in self.hyper_galaxy_image_1d_path_dict:
                hyper_galaxy_image_1d = self.hyper_galaxy_image_1d_path_dict[
                    galaxy_path
                ]

                hyper_noise_1d += hyper_galaxy.hyper_noise_map_from_hyper_images_and_noise_map(
                    hyper_model_image=self.hyper_model_image_1d,
                    hyper_galaxy_image=hyper_galaxy_image_1d,
                    noise_map=self.lens_data.noise_map_1d,
                )

        hyper_noise_map_1d = noise_map_1d + hyper_noise_1d

        return lens_fit.LensDataFit(
            image_1d=image_1d,
            noise_map_1d=hyper_noise_map_1d,
            mask_1d=self.lens_data.mask_1d,
            model_image_1d=self.hyper_model_image_1d,
            grid_stack=self.lens_data.grid_stack,
        )

    @classmethod
    def describe(cls, instance):
        return "Running hyper galaxy fit for HyperGalaxy:\n{}".format(
            instance.hyper_galaxy
        )


def run_hyper(self, data, results=None, mask=None, positions=None):
    """
    Run a fit for each galaxy from the previous phase.
    Parameters
    ----------
    data: LensData
    results: ResultsCollection
        Results from all previous phases
    mask: Mask
        The mask
    positions
    Returns
    -------
    results: HyperGalaxyResults
        A collection of results, with one item per a galaxy
    """
    phase = self.make_hyper_phase()

    mask = setup_phase_mask(
        data=data,
        mask=mask,
        mask_function=cast(phase_imaging.PhaseImaging, phase).mask_function,
        inner_mask_radii=cast(phase_imaging.PhaseImaging, phase).inner_mask_radii,
    )

    lens_data = ld.LensData(
        ccd_data=data,
        mask=mask,
        sub_grid_size=cast(phase_imaging.PhaseImaging, phase).sub_grid_size,
        image_psf_shape=cast(phase_imaging.PhaseImaging, phase).image_psf_shape,
        positions=positions,
        interp_pixel_scale=cast(phase_imaging.PhaseImaging, phase).interp_pixel_scale,
        cluster_pixel_scale=cast(phase_imaging.PhaseImaging, phase).cluster_pixel_scale,
        cluster_pixel_limit=cast(phase_imaging.PhaseImaging, phase).cluster_pixel_limit,
        uses_inversion=cast(phase_imaging.PhaseImaging, phase).uses_inversion,
        uses_cluster_inversion=cast(
            phase_imaging.PhaseImaging, phase
        ).uses_cluster_inversion,
    )

    hyper_model_image_1d = results.last.hyper_model_image_1d_from_mask(
        mask=lens_data.mask_2d
    )
    hyper_galaxy_image_1d_path_dict = results.last.hyper_galaxy_image_1d_path_dict_from_mask(
        mask=lens_data.mask_2d
    )

    hyper_result = copy.deepcopy(results.last)
    hyper_result.variable = hyper_result.variable.copy_with_fixed_priors(
        hyper_result.constant
    )
    hyper_result.analysis.uses_hyper_images = True
    hyper_result.analysis.hyper_model_image_1d = hyper_model_image_1d
    hyper_result.analysis.hyper_galaxy_image_1d_path_dict = (
        hyper_galaxy_image_1d_path_dict
    )

    for path, galaxy in results.last.path_galaxy_tuples:

        optimizer = phase.optimizer.copy_with_name_extension(extension=path[-1])

        optimizer.phase_tag = ""

        # TODO : This is a HACK :O

        optimizer.variable.lens_galaxies = results.last.constant.lens_galaxies

        if hasattr(results.last.constant, "source_galaxies"):
            optimizer.variable.source_galaxies = results.last.constant.source_galaxies

        if hasattr(results.last.constant, "galaxies"):
            optimizer.variable.galaxies = results.last.constant.galaxies

        phase.const_efficiency_mode = af.conf.instance.non_linear.get(
            "MultiNest", "extension_hyper_galaxy_const_efficiency_mode", bool
        )
        phase.optimizer.sampling_efficiency = af.conf.instance.non_linear.get(
            "MultiNest", "extension_hyper_galaxy_sampling_efficiency", float
        )
        phase.optimizer.n_live_points = af.conf.instance.non_linear.get(
            "MultiNest", "extension_hyper_galaxy_n_live_points", int
        )

        optimizer.variable.hyper_galaxy = g.HyperGalaxy

        if self.include_sky_background:
            optimizer.variable.hyper_image_sky = hd.HyperImageSky

        if self.include_noise_background:
            optimizer.variable.hyper_noise_background = hd.HyperNoiseBackground

        # If array is all zeros, galaxy did not have image in previous phase and
        # should be ignored
        if not np.all(hyper_galaxy_image_1d_path_dict[path] == 0):

            analysis = self.Analysis(
                lens_data=lens_data,
                hyper_model_image_1d=hyper_model_image_1d,
                hyper_galaxy_image_1d_path_dict=hyper_galaxy_image_1d_path_dict,
            )

            result = optimizer.fit(analysis)

            def transfer_field(name):
                if hasattr(result.constant, name):
                    setattr(
                        hyper_result.constant.object_for_path(path),
                        name,
                        getattr(result.constant, name),
                    )
                    setattr(
                        hyper_result.variable.object_for_path(path),
                        name,
                        getattr(result.variable, name),
                    )

            transfer_field("hyper_galaxy")
            transfer_field("hyper_image_sky")
            transfer_field("hyper_noise_background")

    return hyper_result
