from setuptools import setup

setup(
    app=["BLE_Windows_Mac.py"],
    setup_requires=["py2app"],
    options=dict(
        py2app=dict(
            plist=dict(
                NSBluetoothAlwaysUsageDescription="This app uses Bluetooth.",
            ),
        ),
    ),
)