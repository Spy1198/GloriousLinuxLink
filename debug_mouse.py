import hid

def wired_force_test():
    # ID for Model D Wireless
    vid, pid = 0x258a, 0x2012
    
    # We are looking specifically for the 'Usage Page' that handles configuration
    # On Linux, this is usually mapped to interface 2
    for device_info in hid.enumerate(vid, pid):
        if device_info['interface_number'] == 2:
            print(f"Trying to wake up Interface 2 at {device_info['path']}...")
            try:
                dev = hid.device()
                dev.open_path(device_info['path'])
                
                # Send a 'Vendor Specific' wake-up call
                # This often bypasses the 'Wired Lock'
                dev.send_feature_report([0x04, 0x01, 0x00, 0x00, 0x00])
                
                # Try to read battery status
                dev.send_feature_report([0x04, 0x02, 0x02, 0x00])
                data = dev.get_feature_report(0x04, 64)
                
                raw = list(data)
                print(f"RESPONSE: {raw}")
                
                if any(x != 0 for x in raw):
                    print("SUCCESS! Data found.")
                else:
                    print("Still zeros. The mouse firmware might be locking the port.")
                
                dev.close()
            except Exception as e:
                print(f"Failed: {e}")

if __name__ == "__main__":
    wired_force_test()
