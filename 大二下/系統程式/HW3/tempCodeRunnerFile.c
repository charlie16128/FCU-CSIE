    // ret = process_line(&line);
    // if (ret != LINE_EOF && strcmp(line.op, "START") == 0) {
    //     start_address = (int)strtol(line.operand1, NULL, 16);
    //     LOCCTR = start_address;
    //     // 印出第一行 (需求 1)
    //     printf("%06X  %-10s %-10s %-10s\n", LOCCTR, line.symbol, line.op, line.operand1);
        
    //     // 如果 START 有 Symbol 就存入
    //     if (strlen(line.symbol) > 0) add_to_symtab(line.symbol, LOCCTR);
        
    //     ret = process_line(&line);
    // }