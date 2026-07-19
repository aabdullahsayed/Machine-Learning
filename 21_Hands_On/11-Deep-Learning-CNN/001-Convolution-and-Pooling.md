# 001 - Convolution and Pooling

## Concept
A convolution slides a small learnable filter (kernel) across an image, computing a weighted sum at each position to detect local patterns (edges, textures). Pooling then downsamples the result, keeping the strongest signals while shrinking the spatial size and adding translation tolerance.

## Why It Matters
Convolutions are why CNNs handle images far more efficiently than fully-connected layers: they share weights across the whole image and exploit the fact that nearby pixels are related, drastically cutting parameter count.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. A simple 2D convolution implemented from scratch
def convolve2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode="constant")
    ih, iw = image.shape
    kh, kw = kernel.shape
    oh = (ih - kh) // stride + 1
    ow = (iw - kw) // stride + 1
    output = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            region = image[i*stride:i*stride+kh, j*stride:j*stride+kw]
            output[i, j] = np.sum(region * kernel)
    return output

# 2. A toy 8x8 "image" with a vertical edge
image = np.array([
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
    [0,0,0,1,1,1,1,1],
], dtype=float)

# 3. Classic edge-detection kernels
vertical_edge_kernel = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
horizontal_edge_kernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
blur_kernel = np.ones((3, 3)) / 9

edges_v = convolve2d(image, vertical_edge_kernel)
edges_h = convolve2d(image, horizontal_edge_kernel)
blurred = convolve2d(image, blur_kernel)

print("Vertical edge detection output:\n", edges_v)

fig, axes = plt.subplots(1, 4, figsize=(14, 4))
for ax, img, title in zip(axes, [image, edges_v, edges_h, blurred],
                           ["Original", "Vertical edges", "Horizontal edges", "Blurred"]):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.savefig("convolution_demo.png")
plt.close()

# 4. Effect of stride and padding on output size
for stride in [1, 2]:
    for padding in [0, 1]:
        out = convolve2d(image, vertical_edge_kernel, stride=stride, padding=padding)
        print(f"stride={stride}, padding={padding}: output shape={out.shape}")

# 5. Max pooling - downsamples while keeping the strongest activation in each window
def max_pool2d(feature_map, pool_size=2, stride=2):
    h, w = feature_map.shape
    oh = (h - pool_size) // stride + 1
    ow = (w - pool_size) // stride + 1
    output = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            region = feature_map[i*stride:i*stride+pool_size, j*stride:j*stride+pool_size]
            output[i, j] = np.max(region)
    return output

pooled = max_pool2d(edges_v, pool_size=2, stride=2)
print("Feature map shape before pooling:", edges_v.shape)
print("Feature map shape after 2x2 max pooling:", pooled.shape)
```

## Exercise
1. Design your own 3x3 kernel that detects diagonal edges and test it on the toy image.
2. Implement `avg_pool2d` alongside `max_pool2d` and compare their outputs on the same feature map — when might average pooling be preferable?
3. Compute the output shape formula `(W - K + 2P) / S + 1` by hand for a 32x32 image, 5x5 kernel, stride 1, padding 2 — then verify it with `convolve2d`.

## Key Takeaways
- A convolution kernel is just a small matrix of learnable weights — in a real CNN, the network learns what patterns each kernel should detect, rather than you hand-designing them like the edge detectors above.
- Stride controls how far the kernel moves each step; padding controls whether the output shrinks (valid) or stays the same size (same) as the input.
- Pooling reduces spatial dimensions and provides a degree of translation invariance (a slightly shifted feature still triggers a similar pooled output), while cutting computation for later layers.
