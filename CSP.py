import re

# Tach input thanh cac thanh phan
# Vi du: "SEND + MORE = MONEY" --> ["SEND", "MORE", "MONEY", "+"]
def parse_equation(equation):
    parts = re.split(r'[+\-=]', equation)
    operands = [part.strip() for part in parts[:-1]]
    result = parts[-1].strip()
    operator = ""
    if '+' in equation:
        operator = '+'
    elif '-' in equation:
        operator = '-'
    else:
        raise ValueError("Unsupported operation. Only + and - are supported.\n")
    return operands, result, operator

# Chuyen chuoi thanh so nguyen dua vao bang gan
def to_numeric(str, assignment):
    number = 0
    for char in str:
        if char in assignment:
            number = number * 10 + assignment[char]
        else:
            return None
    return number

# Kiem tra cac gia tri gan co thoa man phep tinh
def check_equation(operands, result, operator, assignment):
    # Kiem tra chu cai dau khong duoc la 0
    for operand in operands:
        if operand[0] in assignment and assignment[operand[0]] == 0:
            return False
    if result[0] in assignment and assignment[result[0]] == 0:
        return False
    
    # Chuyen cac operands va result thanh so
    operand_values = [to_numeric(op, assignment) for op in operands]
    result_value = to_numeric(result, assignment)
    
    # Neu co bat ky gia tri nao chua duoc gan hoac khong hop le
    if result_value is None or None in operand_values:
        return False
    
    # Kiem tra phep tinh
    if operator == '+':
        return sum(operand_values) == result_value
    else:  # operator == '-'
        return operand_values[0] - operand_values[1] == result_value

# Su dung thuat toan quay lui de tim to hop gia tri cho cac chu cai
def solve_csp(operands, result, operator, letters, first_letters, domains, assignment):
    # Kiem tra neu da gan gia tri cho tat ca cac chu cai
    if len(assignment) == len(letters):
        return check_equation(operands, result, operator, assignment)
    
    # Chon chu cai chua duoc gan gia tri
    unassigned_letters = [letter for letter in letters if letter not in assignment]
    letter = unassigned_letters[0]
    
    # Thu tung gia tri co the gan cho chu cai
    for value in domains[letter][:]:  # sao chep danh sach de tranh thay doi ban goc
        # Gan gia tri cho chu cai
        assignment[letter] = value
        
        # Luu tru domains hien tai va cap nhat
        temp_domains = {}
        for l in letters:
            if l not in assignment:  # Luu lai domain cho cac chu cai chua duoc gan
                temp_domains[l] = domains[l][:]
                
                # Loai cac gia tri da gan khoi domain
                if value in domains[l]:
                    domains[l].remove(value)
        
        # Tiep tuc gan gia tri cho chu cai tiep theo
        if solve_csp(operands, result, operator, letters, first_letters, domains, assignment):
            return True
        
        # Quay lui: xoa gia tri da gan
        del assignment[letter]
        
        # Khoi phuc domains
        for l in temp_domains:
            domains[l] = temp_domains[l]
    
    # Khong tim thay loi giai
    return False
