# miniatures

Programmatically implementing the tilt shift effect to create fake miniatures from a normal image.

![Example](https://i.imgur.com/1W4llxH.png)

## Background

The tilt shift effect is often used in architectural photography. The idea is to use a normal camera on small and medium formats, to create what would be a normal view into a "miniature view". To do this on a normal camera, you would rotate the lens plane relative to the image plane (giving the name tilt), and move the lens parallel to the image plane (giving the name shift). The problem with this is that it requires modifying your lens and you cannot backtrack what would be a normal image. The idea behind this project is to have this same effect, but do this post-algorithmically using a Python program. 

## Algorithm

The algorithm to achieve this effect is very simple. First we take the image and increase the saturation and brightness of the colors, giving a "dream like" feeling to the items in the image. After this, we programmaticaly determine how large we want our focus line to be, and thus generate a mask. After generating a mask we blend the outer layers using a Gaussian mask, and the proceed inwards until the image is clear. We apply this filter on top, thus giving our miniature.  

## Running the Code

### Normal Mask
```
python <path/to/image>
```
### Custom Mask
```
python <path/to/image> <path/to/mask>
```



