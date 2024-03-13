import subprocess
import json

def read_co2_pwm():
    command = "python -m mh_z19 --pwm --pwm_gpio 12 --pwm_range 2000"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    #Ouput comes in Bytes, the following is to convert to dict, then extract co2 value
    output_str = output.decode('utf-8')
    datos_dict = eval(output_str)
    co2_value = datos_dict['co2']
    return co2_value

def main():
        error = False
        data = {
                'Co2': 0,
                'error': error
        }
        try:
                co2_data = read_co2_pwm()
                data['Co2'] = co2_data
        except:
                print("Error Reading Values from MH_zh19")
                data['error'] = True

        print(json.dumps(data, indent= 4))

if __name__ == "__main__":
    main()
