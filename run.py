import subprocess

if __name__ == '__main__':
    process_streamlit = subprocess.Popen("streamlit run main.py", shell=True, stderr=subprocess.PIPE)

    process_streamlit.wait()

    print("main.py streamlit errors:", process_streamlit.stderr.read())
