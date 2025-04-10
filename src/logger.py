log_file = open("test_log.log", "a", encoding="utf8") 
def write_log(line_number, row, error):
    log_file.write(f"Error in line {line_number}: {row} \n {error}\n\n")
    log_file.flush()