import random
import noise

xSize = 100
ySize = 100
zSize = 100
Mode = 0
ProbabilityOverride = 0
ColorMode = 0  # 0 random, 1 perlin same seed, 2 perlin different seed

NoFloating = False
Array3D = []
PSize = 0
NoiseToColor = 0
RandomNoiseColorSeed = 0.01
if Mode == 0:
    # Completely random, looks like Ready Player One's housing
    spawnchance = 75
    GenMode = "Random"
elif Mode == 1:
    # Random Islands
    GenMode = "Random"
    spawnchance = 75
    NoFloating = True
elif Mode == 2:
    # Random with Perlin
    GenMode = "Perlin"
    spawnchance = 75
    PSize = 0.05
elif Mode == 3:
    # Perlin No Floating, Looks kind of like island structures
    GenMode = "Perlin"
    spawnchance = 75
    NoFloating = True
    PSize = 0.05
elif Mode == 4:
    # Should be voronoi
    GenMode = "Random"
    spawnchance = 25
else:
    GenMode = "Random"
    spawnchance = 50

if ProbabilityOverride != 0:
    spawnchance = ProbabilityOverride


if GenMode == "Random":
    for i in range(xSize):
        iArray = []
        for j in range(zSize):
            jArray = []
            for k in range(ySize):
                jArray.append([True if random.randint(0, 100) > spawnchance else False, random.randint(0, 14)])
            if jArray[0][0]:
                jArray[0][1] = 15
            iArray.append(jArray)
        Array3D.append(iArray)
elif GenMode == "Perlin":
    Seed = [random.randint(0, 100000), random.randint(0, 100000), random.randint(0, 100000)]
    Seed2 = [random.randint(0, 100000), random.randint(0, 100000), random.randint(0, 100000)]
    for i in range(xSize):
        iArray = []
        for j in range(zSize):
            jArray = []
            for k in range(ySize):
                if ColorMode == 1:
                    NoiseToColor = abs(noise.pnoise3((i * PSize) + Seed[0], (j * PSize) + Seed[1], (k * PSize * 3) + Seed[2])) * 2
                    if NoiseToColor > 1:
                        NoiseToColor = 1.0
                elif ColorMode == 2:
                    NoiseToColor = abs(noise.pnoise3((i * RandomNoiseColorSeed) + Seed2[0], (j * RandomNoiseColorSeed) + Seed2[1], (k * RandomNoiseColorSeed * 3) + Seed2[2])) * 2
                    if NoiseToColor > 1:
                        NoiseToColor = 1.0
                NoiseToColor = int(NoiseToColor * 14)
                jArray.append([True if noise.pnoise3((i * PSize) + Seed[0], (j * PSize) + Seed[1], (k * PSize * 3) + Seed[2]) > 0 else False, random.randint(0, 14) if ColorMode == 0 else NoiseToColor])
            if jArray[0][0]:
                jArray[0][1] = 15
            iArray.append(jArray)
        Array3D.append(iArray)

if NoFloating:
    for n, i in enumerate(Array3D):
        for o, j in enumerate(i):
            AirGap = False
            for p, k in enumerate(j):
                if AirGap:
                    Array3D[n][o][p][0] = False
                if not k[0]:
                    AirGap = True

CornersPy = []
VoxelsPy = []

for n, i in enumerate(Array3D):
    for o, j in enumerate(i):
        TileCount = 0
        for p, k in enumerate(j):
            if k[0]:
                TileCount += 1
                VoxelsPy.append([k[1], p])
        if TileCount > 0:
            CornersPy.append([n * 9, o * 9, TileCount])

CornersXML = ""
for Corner in CornersPy:
    CornersXML += f"\n    <C>\n      <x>{Corner[0]}</x>\n      <y>{Corner[1]}</y>\n      <count>{Corner[2]}</count>\n    </C>"

VoxelsXML = ""
for Voxel in VoxelsPy:
    VoxelsXML += f"\n      <V>\n      <t>{Voxel[0]}</t>\n      <h>{Voxel[1]}</h>\n      </V>"


FinalXML = f"""<?xml version="1.0" encoding="utf-8"?>
<SaveData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <saveString></saveString>
  <cam>
    <x>0</x>
    <y>0</y>
    <z>0</z>
  </cam>
  <corners>{CornersXML}
  </corners>
  <voxels>{VoxelsXML}
  </voxels>
  <smallJpg>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</smallJpg>
  <bigJpg>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</bigJpg>
</SaveData>"""
with open("Town4.scape", "w+") as f:
    f.write(FinalXML)

print(FinalXML)
