#!/usr/bin/env python
import numpy as np
##
# This example shows how to apply an vtkImageData texture to an sphere 
# vtkPolyData object.
# Note: Input jpg file can be located in the VTKData repository.
#
# @author JBallesteros
##
 
import vtk
BACKGROUND_COLOR = (1.0, 1.0, 1.0)  # white
jpegfile = "Map_3D_2D.jpg"
EARTH_RADIUS = 6371000
LANDMASS_OUTLINE_COLOR = (0.0, 0.0, 0.0)  # black, best contrast
EARTH_LAND_OPACITY = 1.0

EARTH_BASE_COLOR = (0.6, 0.6, 0.8)  # light blue, like water!
EARTH_OPACITY = 1.0

BACKGROUND_COLOR = (1.0, 1.0, 1.0)  # white

SAT_COLOR = (1.0, 0.0, 0.0)  # red, color of satellites
SAT_OPACITY = 1.0

GND_COLOR = (0.0, 1.0, 0.0)  # green, color of groundstations
GND_OPACITY = 1.0

ISL_LINK_COLOR = (0.9, 0.5, 0.1)  # yellow-brown, satellite-satellite links
ISL_LINK_OPACITY = 1.0
ISL_LINE_WIDTH = 3  # how wide to draw line in pixels

SGL_LINK_COLOR = (0.5, 0.9, 0.5)  # greenish? satellite-groundstation links
SGL_LINK_OPACITY = 0.75
SGL_LINE_WIDTH = 2  # how wide to draw line in pixels

PATH_LINK_COLOR = (0.8, 0.2, 0.8)  # purpleish? path links
PATH_LINK_OPACITY = 0.7
PATH_LINE_WIDTH = 13  # how wide to draw line in pixels

EARTH_SPHERE_POINTS = 5000  # higher = smoother earth model, slower to generate

SAT_POINT_SIZE = 9  # how big satellites are in (probably) screen pixels
GND_POINT_SIZE = 8  # how big ground points are in (probably) screen pixels

SECONDS_PER_DAY = 86400  # number of seconds per earth rotation (day)

# Generate an sphere polydata
sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(200)
sphere.SetPhiResolution(79)
sphere.SetRadius(EARTH_RADIUS)

sphere.SetStartTheta(0)
epsilon = 1.e-4
sphere.SetEndTheta(360.0 - epsilon)

# Read the image data from a file
reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)

# Create texture object
texture = vtk.vtkTexture()
texture.SetInputConnection(reader.GetOutputPort())

# Map texture coordinates
map_to_sphere = vtk.vtkTextureMapToSphere()
map_to_sphere.SetInputConnection(sphere.GetOutputPort())
map_to_sphere.AutomaticSphereGenerationOn()
# map_to_sphere.PreventSeamOn()
map_to_sphere.PreventSeamOff()

# Create mapper and set the mapped texture as input
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(map_to_sphere.GetOutputPort())

# Create an actor
earthActor = vtk.vtkActor()
earthActor.SetMapper(mapper)
earthActor.SetTexture(texture)



# create a renderer object
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# create an interactor object, to interact with the window... duh
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
interactor.SetRenderWindow(renderWindow)


renderer.AddActor(earthActor)

# white background, makes it easier to
# put screenshots of animation into papers/presentations
renderer.SetBackground(BACKGROUND_COLOR)

interactor.Initialize()
print('initialized interactor')

# set up a timer to call the update function at a max rate
# of every 7 ms (~144 hz)
interactor.CreateRepeatingTimer(7)
print('set up timer')

# start the model
renderWindow.SetSize(512, 512)
renderWindow.Render()
print('started render')
interactor.Start()
print('started interactor')