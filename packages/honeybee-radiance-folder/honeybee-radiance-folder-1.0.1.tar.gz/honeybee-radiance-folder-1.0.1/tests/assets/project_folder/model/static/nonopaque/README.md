# nonopaque geometry

`/model/static/nonopaque`

This folder includes all nonopaque geometries in the model which are not part of the
apertures. The geometries in this folder are usually geometries with transparent or
translucent materials. The files must follow a certain naming convention.

1. `<filename>.rad`: Includes Radiance geometries / surfaces.
2. `<filename>.mat`: Includes Radiance materials / modifiers.

In this sample case the only transparent geometry which is not part of the apertures is
the top part of the partition inside the room.

![nonopaque_indoor](https://user-images.githubusercontent.com/2915573/53506467-05dd6400-3a84-11e9-9d15-a1a859135234.jpg)

Even though this partition could be included in this folder the file for partition is
located in `indoor` sub-folder. It is good practice to separate the indoor and outdoor
geometries into the subfolders. This separation will help to relax the calculation
parameters for view-matrix versus daylight-matrix in multi-phase daylight simulation.
