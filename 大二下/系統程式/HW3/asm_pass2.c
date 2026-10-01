#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "optable.c"

/* Public variables and functions */
#define ADDR_SIMPLE 0x01
#define ADDR_IMMEDIATE 0x02
#define ADDR_INDIRECT 0x04
#define ADDR_INDEX 0x08

#define LINE_EOF (-1)
#define LINE_COMMENT (-2)
#define LINE_ERROR (0)
#define LINE_CORRECT (1)

typedef struct
{
	char symbol[LEN_SYMBOL];
	char op[LEN_SYMBOL];
	char operand1[LEN_SYMBOL];
	char operand2[LEN_SYMBOL];
	unsigned code;
	unsigned fmt;
	unsigned addressing;
} LINE;

int process_line(LINE *line);

void init_LINE(LINE *line)
{
	line->symbol[0] = '\0';
	line->op[0] = '\0';
	line->operand1[0] = '\0';
	line->operand2[0] = '\0';
	line->code = 0x0;
	line->fmt = 0x0;
	line->addressing = ADDR_SIMPLE;
}

int process_line(LINE *line)
{
	char buf[LEN_SYMBOL];
	int c;
	int state;
	int ret;
	Instruction *op;

	c = ASM_token(buf); 
	if (c == EOF)
		return LINE_EOF;
	else if ((c == 1) && (buf[0] == '\n')) 
		return LINE_COMMENT;
	else if ((c == 1) && (buf[0] == '.')) 
	{
		do { c = ASM_token(buf); } while ((c != EOF) && (buf[0] != '\n'));
		return LINE_COMMENT;
	}
	else
	{
		init_LINE(line);
		ret = LINE_ERROR;
		state = 0;
		while (state < 8)
		{
			switch (state)
			{
			case 0:
			case 1:
			case 2:
				op = is_opcode(buf);
				if ((state < 2) && (buf[0] == '+')) 
				{
					line->fmt = FMT4;
					state = 2;
				}
				else if (op != NULL) 
				{
					strcpy(line->op, op->op);
					line->code = op->code;
					state = 3;
					if (line->fmt != FMT4)
						line->fmt = op->fmt & (FMT1 | FMT2 | FMT3);
					else if ((line->fmt == FMT4) && ((op->fmt & FMT4) == 0)) 
					{														 
						printf("ERROR at token %s, %s cannot use format 4 \n", buf, buf);
						ret = LINE_ERROR;
						state = 7; 
					}
				}
				else if (state == 0) 
				{
					strcpy(line->symbol, buf);
					state = 1;
				}
				else 
				{
					printf("ERROR at token %s\n", buf);
					ret = LINE_ERROR;
					state = 7; 
				}
				break;
			case 3:
				if (line->fmt == FMT1 || line->code == 0x4C) 
				{
					if (c == EOF || buf[0] == '\n') { ret = LINE_CORRECT; state = 8; }
					else { ret = LINE_CORRECT; state = 7; }
				}
				else
				{
					if (c == EOF || buf[0] == '\n') { ret = LINE_ERROR; state = 8; }
					else if (buf[0] == '@' || buf[0] == '#')
					{
						line->addressing = (buf[0] == '#') ? ADDR_IMMEDIATE : ADDR_INDIRECT;
						state = 4;
					}
					else 
					{
						op = is_opcode(buf);
						if (op != NULL) {
							printf("Operand1 cannot be a reserved word\n");
							ret = LINE_ERROR; state = 7; 
						} else {
							strcpy(line->operand1, buf); state = 5;
						}
					}
				}
				break;
			case 4:
				op = is_opcode(buf);
				if (op != NULL) {
					printf("Operand1 cannot be a reserved word\n");
					ret = LINE_ERROR; state = 7; 
				} else {
					strcpy(line->operand1, buf); state = 5;
				}
				break;
			case 5:
				if (c == EOF || buf[0] == '\n') { ret = LINE_CORRECT; state = 8; }
				else if (buf[0] == ',') { state = 6; }
				else { ret = LINE_CORRECT; state = 7; }
				break;
			case 6:
				if (c == EOF || buf[0] == '\n') { ret = LINE_ERROR; state = 8; }
				else 
				{
					op = is_opcode(buf);
					if (op != NULL) {
						printf("Operand2 cannot be a reserved word\n");
						ret = LINE_ERROR; state = 7; 
					} else {
						if (line->fmt == FMT2) {
							strcpy(line->operand2, buf);
							ret = LINE_CORRECT; state = 7;
						} else if ((c == 1) && (buf[0] == 'x' || buf[0] == 'X')) {
							line->addressing = line->addressing | ADDR_INDEX;
							ret = LINE_CORRECT; state = 7; 
						} else {
							printf("Operand2 exists only if format 2 is used\n");
							ret = LINE_ERROR; state = 7; 
						}
					}
				}
				break;
			case 7: 
				if (c == EOF || buf[0] == '\n') state = 8;
				break;
			}
			if (state < 8) c = ASM_token(buf); 
		}
		return ret;
	}
}

typedef struct
{
	char symbol[LEN_SYMBOL];
	int address;
} Symbolinfo;

Symbolinfo SYMTAB[100];
int symbol_count = 0;

void add_to_symtab(char *name, int addr)
{
	if (name == NULL || strlen(name) == 0 || name[0] == '\0') return;
	for (int i = 0; i < symbol_count; i++)
		if (strcmp(SYMTAB[i].symbol, name) == 0) return;
	strcpy(SYMTAB[symbol_count].symbol, name);
	SYMTAB[symbol_count].address = addr;
	symbol_count++;
}

int get_sym_address(char *name) 
{
	for (int i = 0; i < symbol_count; i++) 
		if (strcmp(SYMTAB[i].symbol, name) == 0) return SYMTAB[i].address;
	return 0;
}

int is_symbol(char *str) 
{
	for(int i = 0; i < symbol_count; i++) {
		if (strcmp(SYMTAB[i].symbol, str) == 0) return 1;
	}
	return 0; // If not in SYMTAB, it's likely a constant (number)
}

int get_reg_num(char *reg) 
{
	if (strcmp(reg, "A") == 0) return 0;
	if (strcmp(reg, "X") == 0) return 1;
	if (strcmp(reg, "L") == 0) return 2;
	if (strcmp(reg, "B") == 0) return 3;
	if (strcmp(reg, "S") == 0) return 4;
	if (strcmp(reg, "T") == 0) return 5;
	if (strcmp(reg, "F") == 0) return 6;
	return 0;
}

char T_buf[70] = "";
int T_start = 0;
int M_records[100];
int M_count = 0;

void flush_T_record() 
{
	if (strlen(T_buf) > 0) 
	{
		printf("T%06X%02X%s\n", T_start, (int)(strlen(T_buf) / 2), T_buf);
		T_buf[0] = '\0';
	}
}

int main(int argc, char *argv[])
{
	int ret;
	int LOCCTR = 0;
	int start_address = 0;
	int program_length = 0;
	int base_flag = 0;
	int base_register_value = 0;
	LINE line;

	if (argc < 2) { printf("Usage: %s fname.asm\n", argv[0]); return 1; }

	if (ASM_open(argv[1]) == NULL) { printf("File not found!!\n"); return 1; }

	ret = process_line(&line);
	if (ret != LINE_EOF && strcmp(line.op, "START") == 0) {
		start_address = (int)strtol(line.operand1, NULL, 16);
		LOCCTR = start_address;
		if (strlen(line.symbol) > 0) add_to_symtab(line.symbol, LOCCTR);
		ret = process_line(&line);
	}

	while (ret != LINE_EOF)
	{
		if (ret == LINE_COMMENT) { ret = process_line(&line); continue; }
		if (ret == LINE_CORRECT)
		{
			if (line.symbol[0] != '\0') add_to_symtab(line.symbol, LOCCTR);

			if (line.fmt == FMT1) LOCCTR += 1;
			else if (line.fmt == FMT2) LOCCTR += 2;
			else if (line.fmt == FMT3) LOCCTR += 3;
			else if (line.fmt == FMT4) LOCCTR += 4;
			else
			{
				if (strcmp(line.op, "WORD") == 0) LOCCTR += 3;
				else if (strcmp(line.op, "RESW") == 0) LOCCTR += 3 * atoi(line.operand1);
				else if (strcmp(line.op, "RESB") == 0) LOCCTR += atoi(line.operand1);
				else if (strcmp(line.op, "BYTE") == 0) {
					if (line.operand1[0] == 'C') LOCCTR += (strlen(line.operand1) - 3);
					else if (line.operand1[0] == 'X') LOCCTR += (strlen(line.operand1) - 3) / 2;
				}
			}
		}
		if (strcmp(line.op, "END") == 0) break;
		ret = process_line(&line);
	}
	program_length = LOCCTR - start_address;
	ASM_close();

	ASM_open(argv[1]);
	LOCCTR = start_address;
	T_start = start_address;
	
	ret = process_line(&line);
	if (ret != LINE_EOF && strcmp(line.op, "START") == 0)
	{
		printf("H%-6.6s%06X%06X\n", line.symbol, start_address, program_length);	
		ret = process_line(&line);
	}

	while (ret != LINE_EOF)
	{
		if (ret == LINE_COMMENT){ 
			ret = process_line(&line); continue;
		}
		
		if (ret == LINE_CORRECT)
		{
			if (strcmp(line.op, "END") == 0) 
			{
				flush_T_record();
				for (int i = 0; i < M_count; i++) printf("M%06X05\n", M_records[i]);
				int exec_addr = start_address; 
				if (strlen(line.operand1) > 0) exec_addr = get_sym_address(line.operand1);
				printf("E%06X\n", exec_addr);
				break;
			}
			
			char objcode[10] = "";
			int update_loc = 0;

			// Handle Assembler Directives
			if (strcmp(line.op, "BASE") == 0) {
				base_flag = 1;
				base_register_value = get_sym_address(line.operand1);
			} else if (strcmp(line.op, "NOBASE") == 0) {
				base_flag = 0;
			} else if (strcmp(line.op, "RESW") == 0) {
				flush_T_record();
				update_loc = 3 * atoi(line.operand1);
			} else if (strcmp(line.op, "RESB") == 0) {
				flush_T_record();
				update_loc = atoi(line.operand1);
			} else if (strcmp(line.op, "WORD") == 0) {
				int val = atoi(line.operand1) & 0xFFFFFF;
				sprintf(objcode, "%06X", val);
				update_loc = 3;
			} else if (strcmp(line.op, "BYTE") == 0) {
				if (line.operand1[0] == 'C') {
					for (int i = 2; i < strlen(line.operand1) - 1; i++) {
						char hex[3];
						sprintf(hex, "%02X", (unsigned char)line.operand1[i]);
						strcat(objcode, hex);
					}
					update_loc = strlen(line.operand1) - 3;
				} else if (line.operand1[0] == 'X') {
					int len = strlen(line.operand1) - 3;
					strncpy(objcode, &line.operand1[2], len);
					objcode[len] = '\0';
					update_loc = len / 2;
				}
			}
			
			else if (line.code < 0x100) 
			{
				if (line.fmt == FMT1) {
					sprintf(objcode, "%02X", line.code);
					update_loc = 1;
				} 
				else if (line.fmt == FMT2) {
					int r1 = get_reg_num(line.operand1);
					int r2 = get_reg_num(line.operand2); 
					sprintf(objcode, "%04X", (line.code << 8) | (r1 << 4) | r2);
					update_loc = 2;
				} 
				else if (line.fmt == FMT3 || line.fmt == FMT4) {
					int pc = LOCCTR + (line.fmt == FMT4 ? 4 : 3);
					int n = 1, i = 1;
					if ((line.addressing & 0x07) == ADDR_IMMEDIATE) { n = 0; i = 1; }
					else if ((line.addressing & 0x07) == ADDR_INDIRECT) { n = 1; i = 0; }
					
					int x = (line.addressing & ADDR_INDEX) ? 1 : 0;
					int b = 0, p = 0, e = (line.fmt == FMT4) ? 1 : 0;
					int disp = 0;

					if (strlen(line.operand1) == 0) { 
						disp = 0;
					} 
					else if (is_symbol(line.operand1)) {
						int TA = get_sym_address(line.operand1);
						if (e) {
							disp = TA;
							M_records[M_count++] = LOCCTR + 1;
						} else {
							int pcdisp = TA - pc;
							if (pcdisp >= -2048 && pcdisp <= 2047) {
								p = 1; 
								disp = pcdisp & 0xFFF;
							} else {
								int basedisp = TA - base_register_value;
								if (base_flag && basedisp >= 0 && basedisp <= 4095) {
									b = 1;
									disp = basedisp & 0xFFF;
								} else {
									printf("Address error (out of bounds) at %06X\n", LOCCTR);
								}
							}
						}
					} 
					else { 
						int val = atoi(line.operand1);
						disp = e ? (val & 0xFFFFF) : (val & 0xFFF);
					}

					int opcode_ni = (line.code & 0xFC) | (n << 1) | i;
					if (e) {
						int obj_val = (opcode_ni << 24) | (x << 23) | (b << 22) | (p << 21) | (1 << 20) | disp;
						sprintf(objcode, "%08X", obj_val);
						update_loc = 4;
					} else {
						int obj_val = (opcode_ni << 16) | (x << 15) | (b << 14) | (p << 13) | (0 << 12) | disp;
						sprintf(objcode, "%06X", obj_val);
						update_loc = 3;
					}
				}
			}

			if (strlen(objcode) > 0) 
			{
				if (strlen(T_buf) == 0) T_start = LOCCTR; 
				if (strlen(T_buf) + strlen(objcode) > 60) {
					flush_T_record();
					T_start = LOCCTR;
				}
				strcat(T_buf, objcode);
			}
			LOCCTR += update_loc;
		}

		ret = process_line(&line);	
	}
	ASM_close();
	return 0;
}
