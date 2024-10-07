import eos
import numpy as np
import cv2
import os.path as osp


def main():
    """Demo for running the eos fitting from Python."""
    landmarks = read_pts('../bin/data/image_0010.pts')
    image_width = 1280 # Make sure to adjust these when using your own images!
    image_height = 1024
    output_basename = 'out'

    model = eos.morphablemodel.load_model("../share/sfm_shape_3448.bin")
    blendshapes = eos.morphablemodel.load_blendshapes("../share/expression_blendshapes_3448.bin")
    # Create a MorphableModel with expressions from the loaded neutral model and blendshapes:
    morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
                                                                        color_model=eos.morphablemodel.PcaModel(),
                                                                        vertex_definitions=None,
                                                                        texture_coordinates=model.get_texture_coordinates())
    landmark_mapper = eos.core.LandmarkMapper('../share/ibug_to_sfm.txt')
    edge_topology = eos.morphablemodel.load_edge_topology('../share/sfm_3448_edge_topology.json')
    contour_landmarks = eos.fitting.ContourLandmarks.load('../share/ibug_to_sfm.txt')
    model_contour = eos.fitting.ModelContour.load('../share/sfm_model_contours.json')

    print('--> Fitting the shape model to the landmarks.')
    (mesh, pose, shape_coeffs, blendshape_coeffs) = eos.fitting.fit_shape_and_pose(morphablemodel_with_expressions,
        landmarks, landmark_mapper, image_width, image_height, edge_topology, contour_landmarks, model_contour)

    output_path = output_basename + '.obj'
    print(f'--> Writing mesh (without texture) to {output_path}')
    eos.core.write_obj(mesh, output_path)
    print('--> Finihed writing mesh')

    # Now you can use your favourite plotting/rendering library to display the fitted mesh, using the rendering
    # parameters in the 'pose' variable.

    # Or for example extract the texture map, like this:
    image = cv2.imread('../bin/data/image_0010.png')
    out_image = image.copy() # for drawing wireframe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA, 4)  # extract_texture(...) expects a 4-channel image

    print('--> Extracting texture map from image.')
    texturemap = eos.render.extract_texture(mesh, pose, image)

    # Draw the fitted mesh as wireframe, and save the image:
    output_path = output_basename + '_wireframe.png'
    print(f'--> Draw the fitted mesh as wireframe, and save the image to {output_path}')
    out_image = eos.render.draw_wireframe(
        out_image, 
        mesh, 
        pose.get_modelview(), 
        pose.get_projection(), 
        np.array((0, image_height, image_width, -image_height))
    )
    cv2.imwrite(output_path, out_image)
    print('--> Finished drawing wireframe')

    # Save the mesh as textured obj:
    output_path = output_basename + '_with_texture.obj'
    print(f'--> Writing mesh (with texture) to {output_path}')
    eos.core.write_textured_obj(mesh, output_path)
    print('--> Finihed writing mesh')

    # And save the texture as a png:
    output_path = osp.splitext(output_path)[0] + '.texture.png'
    print(f'--> Writing texture to {output_path}')
    cv2.imwrite(output_path, texturemap)
    print('--> Finished writing texture')


def read_pts(filename):
    """A helper function to read the 68 ibug landmarks from a .pts file."""
    lines = open(filename).read().splitlines()
    lines = lines[3:71]

    landmarks = []
    ibug_index = 1  # count from 1 to 68 for all ibug landmarks
    for l in lines:
        coords = l.split()
        landmarks.append(eos.core.Landmark(str(ibug_index), [float(coords[0]), float(coords[1])]))
        ibug_index = ibug_index + 1

    return landmarks

if __name__ == "__main__":
    main()
