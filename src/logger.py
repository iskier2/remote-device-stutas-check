import datetime
log_file = open("test_log.log", "a", encoding="utf8") 
def write_log(line_number, dct, error):
    obj = "object:\n\t" + "\n\t".join([f"{key}: {value}" for key, value in dct.items()])
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{time}] Error in line {line_number} \n{obj} \nmessage: \n\t{error}\n\n")
    log_file.flush()