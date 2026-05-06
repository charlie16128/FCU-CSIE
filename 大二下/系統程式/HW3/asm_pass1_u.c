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
/* return LINE_EOF, LINE_COMMENT, LINE_ERROR, LINE_CORRECT and Instruction information in *line*/

/* Private variable and function */

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
/* return LINE_EOF, LINE_COMMENT, LINE_ERROR, LINE_CORRECT */
{
	char buf[LEN_SYMBOL];
	int c;
	int state;
	int ret;
	Instruction *op;

	c = ASM_token(buf); /* get the first token of a line */
	if (c == EOF)
		return LINE_EOF;
	else if ((c == 1) && (buf[0] == '\n')) /* blank line */
		return LINE_COMMENT;
	else if ((c == 1) && (buf[0] == '.')) /* a comment line */
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
				if ((state < 2) && (buf[0] == '+')) /* + */
				{
					line->fmt = FMT4;
					state = 2;
				}
				else if (op != NULL) /* INSTRUCTION */
				{
					strcpy(line->op, op->op);
					line->code = op->code;
					state = 3;
					if (line->fmt != FMT4)
					{
						line->fmt = op->fmt & (FMT1 | FMT2 | FMT3);
					}
					else if ((line->fmt == FMT4) && ((op->fmt & FMT4) == 0)) /* INSTRUCTION is FMT1 or FMT 2*/
					{														 /* ERROR 20210326 added */
						printf("ERROR at token %s, %s cannot use format 4 \n", buf, buf);
						ret = LINE_ERROR;
						state = 7; /* skip following tokens in the line */
					}
				}
				else if (state == 0) /* SYMBOL */
				{
					strcpy(line->symbol, buf);
					state = 1;
				}
				else /* ERROR */
				{
					printf("ERROR at token %s\n", buf);
					ret = LINE_ERROR;
					state = 7; /* skip following tokens in the line */
				}
				break;
			case 3:
				if (line->fmt == FMT1 || line->code == 0x4C) /* no operand needed */
				{
					if (c == EOF || buf[0] == '\n')
					{
						ret = LINE_CORRECT;
						state = 8;
					}
					else /* COMMENT */
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
					else /* get a symbol */
					{
						op = is_opcode(buf);
						if (op != NULL)
						{
							printf("Operand1 cannot be a reserved word\n");
							ret = LINE_ERROR;
							state = 7; /* skip following tokens in the line */
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
					state = 7; /* skip following tokens in the line */
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
				else /* COMMENT */
				{
					ret = LINE_CORRECT;
					state = 7; /* skip following tokens in the line */
				}
				break;
			case 6:
				if (c == EOF || buf[0] == '\n')
				{
					ret = LINE_ERROR;
					state = 8;
				}
				else /* get a symbol */
				{
					op = is_opcode(buf);
					if (op != NULL)
					{
						printf("Operand2 cannot be a reserved word\n");
						ret = LINE_ERROR;
						state = 7; /* skip following tokens in the line */
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
							state = 7; /* skip following tokens in the line */
						}
						else
						{
							printf("Operand2 exists only if format 2  is used\n");
							ret = LINE_ERROR;
							state = 7; /* skip following tokens in the line */
						}
					}
				}
				break;
			case 7: /* skip tokens until '\n' || EOF */
				if (c == EOF || buf[0] == '\n')
					state = 8;
				break;
			}
			if (state < 8)
				c = ASM_token(buf); /* get the next token */
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
	if (name == NULL || strlen(name) == 0 || name[0] == '\0')
	{
		return;
	}

	// check if exist
	for (int i = 0; i < symbol_count; i++)
	{
		if (strcmp(SYMTAB[i].symbol, name) == 0)
			return;
	}

	strcpy(SYMTAB[symbol_count].symbol, name);
	SYMTAB[symbol_count].address = addr;
	symbol_count++;
}

int main(int argc, char *argv[])
{
	int ret;
	int LOCCTR = 0;
	int start_address = 0;
	LINE line;

	if (argc < 2)
	{
		printf("Usage: %s fname.asm\n", argv[0]);
		return 1;
	}

	if (ASM_open(argv[1]) == NULL)
	{
		printf("File not found!!\n");
		return 1;
	}

	// START
	ret = process_line(&line);
	if (ret != LINE_EOF && strcmp(line.op, "START") == 0)
	{
		start_address = (int)strtol(line.operand1, NULL, 16);
		LOCCTR = start_address;

		printf("%06X  %-10s %-10s %-10s\n", LOCCTR, line.symbol, line.op, line.operand1);

		if (strlen(line.symbol) > 0)
			add_to_symtab(line.symbol, LOCCTR);

		ret = process_line(&line);
	}

	while (ret != LINE_EOF)
	{
		if (ret == LINE_COMMENT)
		{
			ret = process_line(&line);
			continue;
		}

		if (ret == LINE_CORRECT)
		{
			printf("%06X  %-10s %-10s %-10s %-10s\n", LOCCTR, line.symbol, line.op, line.operand1, line.operand2);

			if (line.symbol[0] != '\0')
			{
				add_to_symtab(line.symbol, LOCCTR);
			}

			if (line.fmt == FMT1)
				LOCCTR += 1;
			else if (line.fmt == FMT2)
				LOCCTR += 2;
			else if (line.fmt == FMT3)
				LOCCTR += 3;
			else if (line.fmt == FMT4)
				LOCCTR += 4;
			else
			{
				if (strcmp(line.op, "WORD") == 0)
					LOCCTR += 3;
				else if (strcmp(line.op, "RESW") == 0)
					LOCCTR += 3 * atoi(line.operand1);
				else if (strcmp(line.op, "RESB") == 0)
					LOCCTR += atoi(line.operand1);
				else if (strcmp(line.op, "BYTE") == 0)
				{
					if (line.operand1[0] == 'C')
						LOCCTR += (strlen(line.operand1) - 3);
					else if (line.operand1[0] == 'X')
						LOCCTR += (strlen(line.operand1) - 3) / 2;
				}
			}
		}

		if (strcmp(line.op, "END") == 0)
			break;
		ret = process_line(&line);
	}

	printf("\nProgram length : %06X\n", LOCCTR - start_address);

	for (int i = 0; i < symbol_count; i++)
	{
		printf("%-10s : %06X\n", SYMTAB[i].symbol, SYMTAB[i].address);
	}

	ASM_close();
	return 0;
}

/*
int main(int argc, char *argv[])
{
	int			i, c, line_count;
	char		buf[LEN_SYMBOL];
	LINE		line;

	if(argc < 2)
	{
		printf("Usage: %s fname.asm\n", argv[0]);
	}
	else
	{
		if(ASM_open(argv[1]) == NULL)
			printf("File not found!!\n");
		else
		{
			for(line_count = 1 ; (c = process_line(&line)) != LINE_EOF; line_count++)
			{
				if(c == LINE_ERROR)
					printf("%03d : Error\n", line_count);
				else if(c == LINE_COMMENT)
					printf("%03d : Comment line\n", line_count);
				else
					printf("%03d : %12s %12s %12s,%12s (FMT=%X, ADDR=%X)\n", line_count, line.symbol, line.op, line.operand1, line.operand2, line.fmt, line.addressing);
			}
			ASM_close();
		}
	}
}
*/
