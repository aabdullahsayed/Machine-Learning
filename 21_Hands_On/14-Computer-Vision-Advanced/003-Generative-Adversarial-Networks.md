# 003 - Generative Adversarial Networks

## Concept
A GAN pits two networks against each other: a Generator that tries to create realistic fake images from random noise, and a Discriminator that tries to distinguish real images from the generator's fakes. Trained together, the generator gradually learns to produce increasingly convincing images.

## Why It Matters
GANs pioneered practical generative modeling for images (before diffusion models became dominant) and the adversarial training concept — two networks competing to improve each other — shows up across many areas of ML beyond images.

## Hands-On

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Data - MNIST digits, a classic simple GAN target
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)),   # scale to [-1, 1] to match generator's tanh output
])
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=128, shuffle=True)

LATENT_DIM = 100

# 2. Generator - takes random noise, outputs a fake 28x28 image
class Generator(nn.Module):
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 1024), nn.LeakyReLU(0.2),
            nn.Linear(1024, 28*28), nn.Tanh(),   # tanh output matches normalized [-1,1] images
        )

    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

# 3. Discriminator - takes an image (real or fake), outputs probability it's real
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 1), nn.Sigmoid(),
        )

    def forward(self, img):
        return self.net(img)

generator = Generator().to(device)
discriminator = Discriminator().to(device)

criterion = nn.BCELoss()
optimizer_G = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

# 4. Adversarial training loop
def train_gan(epochs=5):
    for epoch in range(epochs):
        for real_images, _ in train_loader:
            batch_size = real_images.size(0)
            real_images = real_images.to(device)
            real_labels = torch.ones(batch_size, 1).to(device)
            fake_labels = torch.zeros(batch_size, 1).to(device)

            # --- Train Discriminator: tell real from fake ---
            optimizer_D.zero_grad()
            real_loss = criterion(discriminator(real_images), real_labels)

            z = torch.randn(batch_size, LATENT_DIM).to(device)
            fake_images = generator(z)
            fake_loss = criterion(discriminator(fake_images.detach()), fake_labels)

            d_loss = real_loss + fake_loss
            d_loss.backward()
            optimizer_D.step()

            # --- Train Generator: fool the discriminator ---
            optimizer_G.zero_grad()
            g_loss = criterion(discriminator(fake_images), real_labels)  # wants D to say "real"
            g_loss.backward()
            optimizer_G.step()

        print(f"Epoch {epoch+1}: D_loss={d_loss.item():.4f}, G_loss={g_loss.item():.4f}")

train_gan(epochs=5)  # increase substantially for real image quality

# 5. Generate and visualize sample images
generator.eval()
with torch.no_grad():
    z = torch.randn(16, LATENT_DIM).to(device)
    samples = generator(z).cpu()

fig, axes = plt.subplots(4, 4, figsize=(6, 6))
for i, ax in enumerate(axes.flat):
    ax.imshow(samples[i].squeeze(), cmap="gray")
    ax.axis("off")
plt.suptitle("GAN-generated digits")
plt.savefig("gan_samples.png")
```

## Exercise
1. Train for 50+ epochs instead of 5 and compare sample quality — GANs typically need many epochs before outputs look convincing.
2. Track and plot `d_loss` and `g_loss` over training — a healthy GAN usually shows both losses oscillating rather than one collapsing to near-zero.
3. Replace the fully-connected layers with convolutional layers (a DCGAN architecture) using `nn.ConvTranspose2d` in the generator and `nn.Conv2d` in the discriminator — compare image quality.

## Key Takeaways
- The generator never sees real images directly — it only learns from the discriminator's feedback about whether its outputs "look real."
- GAN training is notoriously unstable — if the discriminator gets too good too fast, the generator's gradient signal vanishes ("mode collapse" is a related common failure).
- Modern generative image models (Stable Diffusion, DALL-E) mostly use diffusion-based approaches instead of GANs, but GANs remain useful and much faster at inference time once trained.
