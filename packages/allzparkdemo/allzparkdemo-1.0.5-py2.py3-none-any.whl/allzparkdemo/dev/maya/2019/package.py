# An example of a package referencing something from outside
# of the local package.

name = "maya"
version = "2019.0.0"
requires = []

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

# Cross-platform binaries (i.e. shell scripts)
# are built and deployed with this package.
tools = [
    "maya",
    "mayapy",
    "render",
    "mayabatch",
    "mayagui_lic",
]

_data = {
    "label": "Autodesk Maya",
    "color": "#251",
    "icon": "{root}/resources/icon_{width}x{height}.png",
}


def commands():
    global env
    global alias
    global system

    env.PATH.prepend("{root}/bin")
