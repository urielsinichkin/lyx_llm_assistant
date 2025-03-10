import os
from pathlib import Path
import winreg

def find_lyx_installation():
    """Try to find LyX installation directory from Windows registry."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LyX") as key:
            return winreg.QueryValue(key, None)
    except WindowError:
        return None

def get_possible_pipe_paths():
    """Get list of possible pipe locations."""
    paths = []
    
    # User's AppData locations
    appdata = os.getenv('APPDATA', '')  # Roaming
    localappdata = os.getenv('LOCALAPPDATA', '')
    
    possible_dirs = [
        # LyX 2.3 specific directory (prioritized)
        os.path.join(appdata, 'LyX2.3'),
        # Other possible locations
        os.path.join(appdata, 'LyX'),
        os.path.join(appdata, 'lyx'),
        os.path.join(localappdata, 'LyX'),
        os.path.join(localappdata, 'lyx'),
        os.path.join(os.path.expanduser('~'), '.lyx'),
    ]
    
    # Add paths for each
    for dir_path in possible_dirs:
        paths.append(os.path.join(dir_path, 'lyxpipe'))
    
    return paths

def test_lyx_pipe():
    print("Checking LyX installation and pipe configuration...")
    
    # Try to find LyX installation
    lyx_install_dir = find_lyx_installation()
    if lyx_install_dir:
        print(f"\nFound LyX installation at: {lyx_install_dir}")
    else:
        print("\nCouldn't find LyX installation in registry.")
        print("Please verify LyX is installed correctly.")
    
    # Check all possible pipe locations
    print("\nChecking possible pipe locations:")
    pipe_paths = get_possible_pipe_paths()
    
    found_pipes = False
    for pipe_path in pipe_paths:
        pipe_in = f"{pipe_path}.in"
        pipe_out = f"{pipe_path}.out"
        
        pipe_dir = os.path.dirname(pipe_path)
        
        if os.path.exists(pipe_in) or os.path.exists(pipe_out):
            print(f"\n✓ Found LyX pipes at: {pipe_path}")
            print("Server pipe support is enabled!")
            found_pipes = True
            break
        elif os.path.exists(pipe_dir):
            print(f"\nFound LyX directory at: {pipe_dir}")
            print("But no pipe files found. This might be a good location to use.")
    
    if not found_pipes:
        print("\nNo LyX pipes found. Here's what to do:")
        print("\n1. Open LyX")
        print("2. Go to Tools > Preferences > Paths")
        print("3. Look for 'LyX server pipe' setting")
        print("4. Set it to this path:")
        recommended_path = os.path.join(os.getenv('APPDATA', ''), 'LyX2.3', 'lyxpipe')
        print(f"   {recommended_path}")
        print("\n5. Click Apply")
        print("6. Close LyX completely")
        print("7. Restart LyX")
        
        # The directory should already exist, but let's make sure
        recommended_dir = os.path.dirname(recommended_path)
        if not os.path.exists(recommended_dir):
            try:
                Path(recommended_dir).mkdir(parents=True, exist_ok=True)
                print(f"\nCreated directory: {recommended_dir}")
            except Exception as e:
                print(f"\nError creating directory: {e}")

if __name__ == "__main__":
    test_lyx_pipe() 