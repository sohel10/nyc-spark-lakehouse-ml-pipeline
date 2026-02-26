import os

def validate_output(output_path):

    if not os.path.exists(output_path):
        raise ValueError(f"Output not found: {output_path}")

    if len(os.listdir(output_path)) == 0:
        raise ValueError("Output folder is empty")

    print("Output validation passed")