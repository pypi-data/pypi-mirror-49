import os

import autofit as af
from autolens.model.galaxy import galaxy_model as gm
from autolens.pipeline.phase import phase_imaging
from autolens.pipeline import pipeline as pl
from autolens.model.profiles import light_profiles as lp
from test.integration import integration_util
from test.simulation import simulation_util

test_type = "model_mapper"
test_name = "link_variable_float_to_next_phase"

test_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
output_path = test_path + "output/"
config_path = test_path + "config"
af.conf.instance = af.conf.Config(config_path=config_path, output_path=output_path)


def pipeline():

    integration_util.reset_paths(test_name=test_name, output_path=output_path)
    ccd_data = simulation_util.load_test_ccd_data(
        data_type="lens_only_dev_vaucouleurs", data_resolution="LSST"
    )
    pipeline = make_pipeline(test_name=test_name)
    pipeline.run(data=ccd_data)


def make_pipeline(test_name):

    phase1 = phase_imaging.LensPlanePhase(
        phase_name="phase_1",
        phase_folders=[test_type, test_name],
        lens_galaxies=dict(lens=gm.GalaxyModel(light=lp.EllipticalSersic)),
        optimizer_class=af.MultiNest,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 20
    phase1.optimizer.sampling_efficiency = 0.8

    class MMPhase2(phase_imaging.LensPlanePhase):
        def pass_priors(self, results):

            self.lens_galaxies.lens.light.centre = results.from_phase(
                "phase_1"
            ).variable.lens_galaxies.lens.light.centre

            self.lens_galaxies.lens.light.axis_ratio = results.from_phase(
                "phase_1"
            ).variable.lens_galaxies.lens.light.axis_ratio

    phase2 = MMPhase2(
        phase_name="phase_2",
        phase_folders=[test_type, test_name],
        lens_galaxies=dict(lens=gm.GalaxyModel(light=lp.EllipticalSersic)),
        optimizer_class=af.MultiNest,
    )

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 20
    phase2.optimizer.sampling_efficiency = 0.8

    return pl.PipelineImaging(test_name, phase1, phase2)


if __name__ == "__main__":
    pipeline()
