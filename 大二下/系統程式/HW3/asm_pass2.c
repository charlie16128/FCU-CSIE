#include <stdio.h>
#include <string.h>
#include <stdlib.h>
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
		do
		{
			c = ASM_token(buf);
		} while ((c != EOF) && (buf[0] != '\n'));
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
					{
						line->fmt = op->fmt & (FMT1 | FMT2 | FMT3);
					}
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
				if (line->fmt == FMT1 || line->code == 0x4C) /* no operand needed (e.g., RSUB) */
				{
					if (c == EOF || buf[0] == '\n')
					{
						ret = LINE_CORRECT;
						state = 8;
					}
					else 
					{
						ret = LINE_CORRECT;
						state = 7;
					}
				}
				else
				{
					if (c == EOF || buf[0] == '\n')
					{
						ret = LINE_ERROR;
						state = 8;
					}
					else if (buf[0] == '@' || buf[0] == '#')
					{
						line->addressing = (buf[0] == '#') ? ADDR_IMMEDIATE : ADDR_INDIRECT;
						state = 4;
					}
					else 
					{
						op = is_opcode(buf);
						if (op != NULL)
						{
							printf("Operand1 cannot be a reserved word\n");
							ret = LINE_ERROR;
							state = 7; 
						}
						else
						{
							strcpy(line->operand1, buf);
							state = 5;
						}
					}
				}
				break;
			case 4:
				op = is_opcode(buf);
				if (op != NULL)
				{
					printf("Operand1 cannot be a reserved word\n");
					ret = LINE_ERROR;
					state = 7; 
				}
				else
				{
					strcpy(line->operand1, buf);
					state = 5;
				}
				break;
			case 5:
				if (c == EOF || buf[0] == '\n')
				{
					ret = LINE_CORRECT;
					state = 8;
				}
				else if (buf[0] == ',')
				{
					state = 6;
				}
				else 
				{
					ret = LINE_CORRECT;
					state = 7; 
				}
				break;
			case 6:
				if (c == EOF || buf[0] == '\n')
				{
					ret = LINE_ERROR;
					state = 8;
				}
				else 
				{
					op = is_opcode(buf);
					if (op != NULL)
					{
						printf("Operand2 cannot be a reserved word\n");
						ret = LINE_ERROR;
						state = 7; 
					}
					else
					{
						if (line->fmt == FMT2)
						{
							strcpy(line->operand2, buf);
							ret = LINE_CORRECT;
							state = 7;
						}
						else if ((c == 1) && (buf[0] == 'x' || buf[0] == 'X'))
						{
							line->addressing = line->addressing | ADDR_INDEX;
							ret = LINE_CORRECT;
							state = 7; 
						}
						else
						{
							printf("Operand2 exists only if format 2  is used\n");
							ret = LINE_ERROR;
							state = 7; 
						}
					}
				}
				break;
			case 7: 
				if (c == EOF || buf[0] == '\n')
					state = 8;
				break;
			}
			if (state < 8)
				c = ASM_token(buf); 
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
	{
		if (strcmp(SYMTAB[i].symbol, name) == 0) return;
	}
	strcpy(SYMTAB[symbol_count].symbol, name);
	SYMTAB[symbol_count].address = addr;
	symbol_count++;
}

int get_sym_address(char *name) 
{
	for (int i = 0; i < symbol_count; i++) 
	{
		if (strcmp(SYMTAB[i].symbol, name) == 0) 
			return SYMTAB[i].address;
	}
	return 0; // Not found
}

// Helper variables for T record
char T_buf[70] = "";
int T_start = 0;

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
	LINE line;

	if (argc < 2)
	{
		printf("Usage: %s fname.asm\n", argv[0]);
		return 1;
	}

	// ==========================================
	// PASS 1: Build SYMTAB and compute lengths
	// ==========================================
	if (ASM_open(argv[1]) == NULL)
	{
		printf("File not found!!\n");
		return 1;
	}

	ret = process_line(&line);
	if (ret != LINE_EOF && strcmp(line.op, "START") == 0)
	{
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
				else if (strcmp(line.op, "BYTE") == 0)
				{
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

	// ==========================================
	// PASS 2: Generate Object Code Records
	// ==========================================
	ASM_open(argv[1]); // Reopen to read from the start
	LOCCTR = start_address;
	T_start = start_address;
	
	ret = process_line(&line);
	if (ret != LINE_EOF && strcmp(line.op, "START") == 0)
	{
		// Print H record (Header)
		printf("H%-6.6s%06X%06X\n", line.symbol, start_address, program_length);
		ret = process_line(&line);
	}

	while (ret != LINE_EOF)
	{
		if (ret == LINE_COMMENT) { ret = process_line(&line); continue; }
		
		if (ret == LINE_CORRECT)
		{
			// ======== [修正] 提早攔截 END，確保不把它當指令處理 ========
			if (strcmp(line.op, "END") == 0) 
			{
				flush_T_record();
				// E record execution starting address
				int exec_addr = start_address; 
				if (strlen(line.operand1) > 0) 
					exec_addr = get_sym_address(line.operand1);
				
				printf("E%06X\n", exec_addr);
				break;
			}
			
			char objcode[10] = "";
			int update_loc = 0;

			if (strcmp(line.op, "RESW") == 0) 
			{
				flush_T_record();
				update_loc = 3 * atoi(line.operand1);
			}
			else if (strcmp(line.op, "RESB") == 0) 
			{
				flush_T_record();
				update_loc = atoi(line.operand1);
			}
			else if (strcmp(line.op, "WORD") == 0) 
			{
				int val = atoi(line.operand1) & 0xFFFFFF;
				sprintf(objcode, "%06X", val);
				update_loc = 3;
			}
			else if (strcmp(line.op, "BYTE") == 0) 
			{
				if (line.operand1[0] == 'C') 
				{
					for (int i = 2; i < strlen(line.operand1) - 1; i++) 
					{
						char hex[3];
						sprintf(hex, "%02X", (unsigned char)line.operand1[i]);
						strcat(objcode, hex);
					}
					update_loc = strlen(line.operand1) - 3;
				} 
				else if (line.operand1[0] == 'X') 
				{
					int len = strlen(line.operand1) - 3;
					strncpy(objcode, &line.operand1[2], len);
					objcode[len] = '\0';
					update_loc = len / 2;
				}
			}
			// ======== [修正] 加了 line.code < 0x100 的檢查，排除 BASE 等虛擬指令 ========
			else if (line.code < 0x100) 
			{
				int obj_val = line.code << 16; 
				if (strlen(line.operand1) > 0) 
				{
					int addr = get_sym_address(line.operand1);
					if (line.addressing & ADDR_INDEX) addr += 0x8000; // Add index bit
					obj_val |= (addr & 0xFFFF);
				}
				sprintf(objcode, "%06X", obj_val);
				
				if (line.fmt == FMT1) update_loc = 1;
				else if (line.fmt == FMT2) update_loc = 2;
				else if (line.fmt == FMT3) update_loc = 3;
				else if (line.fmt == FMT4) update_loc = 4;
			}

			// Add objcode to T record buffer
			if (strlen(objcode) > 0) 
			{
				if (strlen(T_buf) == 0) T_start = LOCCTR; // Start new T record block
				
				// Max T record size is 30 bytes (60 hex chars)
				if (strlen(T_buf) + strlen(objcode) > 60) 
				{
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

/*
My answer:
HCOPY  00100000107A
T0010001E1410334820390010362810303010154820613C100300102A0C103900102D
T00101E150C10364820610810334C0000454F46000003000000
T0020391E041030001030E0205D30203FD8205D2810303020575490392C205E38203F
T0020571C1010364C0000F1001000041030E02079302064509039DC20792C1036
T002073073820644C000005
E001000

ANS:
HCOPY  00100000107A
T0010001E1410334820390010362810303010154820613C100300102A0C103900102D
T00101E150C10364820610810334C0000454F46000003000000
T0020391E041030001030E0205D30203FD8205D2810303020575490392C205E38203F
T0020571C1010364C0000F1001000041030E02079302064509039DC20792C1036
T002073073820644C000005
E001000
*/