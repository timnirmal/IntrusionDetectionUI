import subprocess

if __name__ == '__main__':
    # Start run_cicflow.py in a background process
    # process_cicflow = subprocess.Popen("python run_cicflow.py", shell=True, stderr=subprocess.PIPE)

    # Start main.py streamlit in a background process
    process_streamlit = subprocess.Popen("streamlit run main.py", shell=True, stderr=subprocess.PIPE)

    # Wait for the subprocesses to finish (optional)
    # process_cicflow.wait()
    process_streamlit.wait()

    # Print standard error output (if any)
    # print("run_cicflow.py errors:", process_cicflow.stderr.read())
    print("main.py streamlit errors:", process_streamlit.stderr.read())
