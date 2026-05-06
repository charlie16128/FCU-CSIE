#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define	LEN_SYMBOL	(20)
#define	TRUE			(1)
#define	FALSE			(0)

#define	FMT0		0x00		/* SIC Assembler Directive */
#define	FMT1		0x01		/* Format 1 */
#define	FMT2		0x02		/* Format 2 */
#define	FMT3		0x04		/* Format 3 */
#define	FMT4		0x08		/* Format 4 */
#define	OP_BYTE	0x101
#define	OP_WORD	0x102
#define	OP_RESB	0x103
#define	OP_RESW	0x104
#define	OP_BASE	0x105
#define	OP_NOBASE	0x106
#define	OP_START	0x107
#define	OP_END		0x108

#define	ADDR_SIMPLE			0x01
#define	ADDR_IMMEDIATE		0x02
#define	ADDR_INDIRECT		0x04
#define	ADDR_INDEX			0x08
#define	LINE_EOF			(-1)
#define	LINE_COMMENT		(-2)
#define	LINE_ERROR			(0)
#define	LINE_CORRECT		(1)

/* Public variables and functions */
FILE *ASM_open(char *fname);		/* Open a SIC/XE asm file */
	/* return NULL if failed */
void	ASM_close(void);				/* Cloase the asm file */
int	ASM_token(char *buf);			/* Get a token from the file */
	/* The token is stored at buf. */
	/* Return the length of the token. Return EOF if end of file reached. */

/* Private variable and functions */
FILE		*ASM_fp;
int		ASM_buf;
int		ASM_flag = FALSE;
char		DELIMITER[] = " ,\t\r\n";
int		LEN_DELIMITER = sizeof(DELIMITER)-1;	/* subtract the last character '\0' */
char		SPECIAL[] = "#@+*,.";					/* , in DELIMINTER and SPECIAL */
int		LEN_SPECIAL = sizeof(SPECIAL)-1;		/* subtract the last character '\0' */

FILE	 *ASM_open(char *fname)
{
	ASM_fp = fopen(fname, "r");
	return (ASM_fp); 
}

void ASM_close(void)
{
	fclose(ASM_fp);
}

int ASM_getc(void)
{
	if(ASM_flag)	/* ASM_buf contains a char */
	{
		ASM_flag = FALSE;
		return(ASM_buf);
	}
	return(fgetc(ASM_fp));
}

void ASM_ungetc(int c)
{
	ASM_flag = TRUE;
	ASM_buf = c;
}

int is_delimiter(int c)
{
	int	i;
	
	for(i = 0 ; i < LEN_DELIMITER ; i++)
		if(c == DELIMITER[i])
			return TRUE;
	return FALSE;
}

int is_special(int c)
{
	int		i;
	
	for(i = 0 ; i < LEN_SPECIAL ; i++)
		if(c == SPECIAL[i])
			return TRUE;
	return FALSE;
}

int ASM_token(char *buf)
/* The token is stored at buf. */
/* Return the length of the token. Return EOF if end of file reached. */
{
	int	c;
	int	len;
	
	buf[0] = '\0';
	/* skip blank character */
	c = ASM_getc();
	while(c == ' ' || c == '\t')
	{
		c = ASM_getc();
	}	
	if(c == EOF)
		return(EOF);
	
	/* now c is the first char of a symbol */
	if(is_special(c))
	{
		buf[0] = c;
		buf[1] = '\0';
		len = 1;
	}
	else if(c == '\r' || c == '\n')
	{
		c = ASM_getc();
		if(c != '\r' && c != '\n')
			ASM_ungetc(c);
		buf[0] = '\n';
		buf[1] = '\0';
		len = 1;
	}
	else
	{
		for(len = 0 ; !is_delimiter(c) && c != EOF; c = ASM_getc())
		{
			if(len < LEN_SYMBOL-1)
			{
				buf[len] = c;
				len++;
			}
		}	
		buf[len] = '\0';
		
		if(c != ' ' && c != '\t')
			ASM_ungetc(c);
	}
	return(len);
}

typedef struct
{
	char		op[LEN_SYMBOL];
	unsigned	fmt;
	unsigned	code;
} Instruction;

Instruction *is_opcode(char *op);
/* retuen pointer to OPTAB[i] if it is found, else return NULL */

/* Private variable and functions */
Instruction	OPTAB[] = {
	{"ADD",		FMT3 | FMT4, 	0x18},
	{"ADDF", 		FMT3 | FMT4,	0x58},
	{"ADDR",		FMT2,		0x90},
	{"AND",		FMT3 | FMT4,	0x40},
	{"BASE",		FMT0,		OP_BASE},
	{"BYTE",		FMT0,		OP_BYTE},
	{"CLEAR",	FMT2,		0xB4},	
	{"COMP",		FMT3 | FMT4, 0x28}, 
	{"COMPF",	FMT3 | FMT4,	0x88},	
	{"COMPR",	FMT2,		0xA0},	
	{"DIV",		FMT3 | FMT4,	0x24},
	{"DIVF",		FMT3 | FMT4,	0x64},	
	{"DIVR",		FMT2,		0x9C},
	{"END",		FMT0,		OP_END},	
	{"FIX",		FMT1,		0xC4},
	{"FLOAT",	FMT1,		0xC0},	
	{"HIO",		FMT1,		0xF4},	
	{"J",			FMT3 | FMT4,	0x3C},
	{"JEQ",		FMT3 | FMT4,	0x30},	
	{"JGT",		FMT3 | FMT4,	0x34},	
	{"JLT",		FMT3 | FMT4,	0x38},
	{"JSUB",		FMT3 | FMT4,	0x48},	
	{"LDA",		FMT3 | FMT4,	0x00},	
	{"LDB",		FMT3 | FMT4,	0x68},
	{"LDCH",		FMT3 | FMT4,	0x50},	
	{"LDF",		FMT3 | FMT4,	0x70},	
	{"LDL",		FMT3 | FMT4,	0x08},
	{"LDS",		FMT3 | FMT4,	0x6C},	
	{"LDT",		FMT3 | FMT4,	0x74},	
	{"LDX",		FMT3 | FMT4,	0x04},
	{"LPS",		FMT3 | FMT4,	0xD0},
	{"MUL",		FMT3 | FMT4,	0x20},	
	{"MULF",		FMT3 | FMT4,	0x60},
	{"MULR",		FMT2,		0x98},
	{"NOBASE",	FMT0,		OP_NOBASE},	
	{"NORM",		FMT1,		0xC8},	
	{"OR",		FMT3 | FMT4,	0x44},
	{"RD",		FMT3 | FMT4,	0xD8},
	{"RESB",		FMT0,		OP_RESB},
	{"RESW",		FMT0,		OP_RESW},	
	{"RMO",		FMT2,		0xAC},	
	{"RSUB",		FMT3 | FMT4,	0x4C},
	{"SHIFTL",	FMT2,		0xA4},	
	{"SHIFTR",	FMT2,		0xA8},	
	{"SIO",		FMT1,		0xF0},
	{"SSK",		FMT3 | FMT4,	0xEC},	
	{"STA",		FMT3 | FMT4,	0x0C},	
	{"START",	FMT0,		OP_START},
	{"STB",		FMT3 | FMT4,	0x78},
	{"STCH",		FMT3 | FMT4,	0x54},	
	{"STF",		FMT3 | FMT4,	0x80},	
	{"STI",		FMT3 | FMT4,	0xD4},
	{"STL",		FMT3 | FMT4,	0x14},	
	{"STS",		FMT3 | FMT4,	0x7C},	
	{"STSW",		FMT3 | FMT4,	0xE8},
	{"STT",		FMT3 | FMT4,	0x84},	
	{"STX",		FMT3 | FMT4,	0x10},	
	{"SUB",		FMT3 | FMT4,	0x1C},
	{"SUBF",		FMT3 | FMT4,	0x5C},	
	{"SUBR",		FMT2,		0x94},	
	{"SVC",		FMT2,		0xB0},
	{"TD",		FMT3 | FMT4,	0xE0},	
	{"TIO",		FMT1,		0xF8},	
	{"TIX",		FMT3 | FMT4,	0x2C},
	{"TIXR",		FMT2,		0xB8},	
	{"WD",		FMT3 | FMT4,	0xDC},
	{"WORD",	FMT0,		OP_WORD}				
};

int LEN_OPTAB = sizeof(OPTAB) / sizeof(Instruction);

Instruction *is_opcode(char *op)
/* retuen pointer to OPTAB[i] if it is found, else return NULL */
{
	int		begin = 0;
	int		end = LEN_OPTAB - 1;
	int		mid, c;
	char		buf[LEN_SYMBOL];
	char		*p;
	
	/* Translate lowercase to capital */
	for(c = 0, p = op ; *p != '\0' ; c++, p++)
	{
		if(*p <= 'z' && *p >= 'a')
			buf[c] = *p - 'a' + 'A';
		else
			buf[c] = *p;
	} 
	buf[c] = '\0';
	
	/* binary search */
	while(begin <= end)
	{
		mid = (begin + end)/2;
		c = strcmp(buf, OPTAB[mid].op);
		if(c == 0)
			return &(OPTAB[mid]);		/* found */
		else if(c < 0)
			end = mid - 1;
		else
			begin = mid + 1;
	}
	return NULL;	/* not found */
}

typedef struct
{
	char		symbol[LEN_SYMBOL];
	char		op[LEN_SYMBOL];
	char		operand1[LEN_SYMBOL];
	char		operand2[LEN_SYMBOL];
	unsigned	code;
	unsigned	fmt;
	unsigned	addressing;	
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
	char		buf[LEN_SYMBOL];
	int			c;
	int			state;
	int			ret;
	Instruction	*op;
	
	c = ASM_token(buf);		/* get the first token of a line */
	if(c == EOF)
		return LINE_EOF;
	else if((c == 1) && (buf[0] == '\n'))	/* blank line */
		return LINE_COMMENT;
	else if((c == 1) && (buf[0] == '.'))	/* a comment line */
	{
		do
		{
			c = ASM_token(buf);
		} while((c != EOF) && (buf[0] != '\n'));
		return LINE_COMMENT;
	}
	else
	{
		init_LINE(line);
		ret = LINE_ERROR;
		state = 0;
		while(state < 8)
		{
			switch(state)
			{
				case 0:
				case 1:
				case 2:
					op = is_opcode(buf);
					if((state < 2) && (buf[0] == '+'))	/* + */
					{
						line->fmt = FMT4;
						state = 2;
					}
					else	if(op != NULL)	/* INSTRUCTION */
					{
						strcpy(line->op, op->op);
						line->code = op->code;
						state = 3;
						if(line->fmt != FMT4)
						{
							line->fmt = op->fmt & (FMT1 | FMT2 | FMT3);
						}
						else if((line->fmt == FMT4) && ((op->fmt & FMT4) == 0)) /* INSTRUCTION is FMT1 or FMT 2*/
						{	/* ERROR 20210326 added */
							printf("ERROR at token %s, %s cannot use format 4 \n", buf, buf);
							ret = LINE_ERROR;
							state = 7;		/* skip following tokens in the line */
						}
					}				
					else	if(state == 0)	/* SYMBOL */
					{
						strcpy(line->symbol, buf);
						state = 1;
					}
					else		/* ERROR */
					{
						printf("ERROR at token %s\n", buf);
						ret = LINE_ERROR;
						state = 7;		/* skip following tokens in the line */
					}
					break;	
				case 3:
					if(line->fmt == FMT1 || line->code == 0x4C)	/* no operand needed */
					{
						if(c == EOF || buf[0] == '\n')
						{
							ret = LINE_CORRECT;
							state = 8;
						}
						else		/* COMMENT */
						{
							ret = LINE_CORRECT;
							state = 7;
						}
					}
					else
					{
						if(c == EOF || buf[0] == '\n')
						{
							ret = LINE_ERROR;
							state = 8;
						}
						else	if(buf[0] == '@' || buf[0] == '#')
						{
							line->addressing = (buf[0] == '#') ? ADDR_IMMEDIATE : ADDR_INDIRECT;
							state = 4;
						}
						else	/* get a symbol */
						{
							op = is_opcode(buf);
							if(op != NULL)
							{
								printf("Operand1 cannot be a reserved word\n");
								ret = LINE_ERROR;
								state = 7; 		/* skip following tokens in the line */
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
					if(op != NULL)
					{
						printf("Operand1 cannot be a reserved word\n");
						ret = LINE_ERROR;
						state = 7;		/* skip following tokens in the line */
					}
					else
					{
						strcpy(line->operand1, buf);
						state = 5;
					}
					break;
				case 5:
					if(c == EOF || buf[0] == '\n')
					{
						ret = LINE_CORRECT;
						state = 8;
					}
					else if(buf[0] == ',')
					{
						state = 6;
					}
					else	/* COMMENT */
					{
						ret = LINE_CORRECT;
						state = 7;		/* skip following tokens in the line */
					}
					break;
				case 6:
					if(c == EOF || buf[0] == '\n')
					{
						ret = LINE_ERROR;
						state = 8;
					}
					else	/* get a symbol */
					{
						op = is_opcode(buf);
						if(op != NULL)
						{
							printf("Operand2 cannot be a reserved word\n");
							ret = LINE_ERROR;
							state = 7;		/* skip following tokens in the line */
						}
						else
						{
							if(line->fmt == FMT2)
							{
								strcpy(line->operand2, buf);
								ret = LINE_CORRECT;
								state = 7;
							}
							else if((c == 1) && (buf[0] == 'x' || buf[0] == 'X'))
							{
								line->addressing = line->addressing | ADDR_INDEX;
								ret = LINE_CORRECT;
								state = 7;		/* skip following tokens in the line */
							}
							else
							{
								printf("Operand2 exists only if format 2  is used\n");
								ret = LINE_ERROR;
								state = 7;		/* skip following tokens in the line */
							}
						}
					}
					break;
				case 7:	/* skip tokens until '\n' || EOF */
					if(c == EOF || buf[0] =='\n')
						state = 8;
					break;										
			}
			if(state < 8)
				c = ASM_token(buf);  /* get the next token */
		}
		return ret;
	}
}
typedef struct {
    char symbol[LEN_SYMBOL];
    int  address;
} Symbolinfo;

Symbolinfo SYMTAB[100];

int symbol_count = 0;

void add_to_symtab(char *name, int addr) {
    if (name == NULL || strlen(name) == 0 || name[0] == '\0') {
        return;
    }
    
    // check if exist
    for(int i = 0; i < symbol_count; i++) {
        if(strcmp(SYMTAB[i].symbol, name) == 0) return;
    }

    strcpy(SYMTAB[symbol_count].symbol, name);
    SYMTAB[symbol_count].address = addr;
    symbol_count++;
}

int main(int argc, char *argv[]) {
    int ret;
    int LOCCTR = 0;
    int start_address = 0;
    LINE line;

    if (argc < 2) {
        printf("Usage: %s fname.asm\n", argv[0]);
        return 1;
    }

    if (ASM_open(argv[1]) == NULL) {
        printf("File not found!!\n");
        return 1;
    }

    // START
    ret = process_line(&line);
    if (ret != LINE_EOF && strcmp(line.op, "START") == 0) {
        start_address = (int)strtol(line.operand1, NULL, 16);
        LOCCTR = start_address;

		printf("%06X  %-10s %-10s %-10s\n", LOCCTR, line.symbol, line.op, line.operand1);
        
        if (strlen(line.symbol) > 0) add_to_symtab(line.symbol, LOCCTR);
        
        ret = process_line(&line);
    }
	
    while (ret != LINE_EOF) {
        if (ret == LINE_COMMENT) {
            ret = process_line(&line);
            continue;
        }

        if (ret == LINE_CORRECT) {
            printf("%06X  %-10s %-10s %-10s %-10s\n", LOCCTR, line.symbol, line.op, line.operand1, line.operand2);	

            if (line.symbol[0] != '\0') {
                add_to_symtab(line.symbol, LOCCTR);
            }

            if (line.fmt == FMT1) LOCCTR += 1;
            else if (line.fmt == FMT2) LOCCTR += 2;
            else if (line.fmt == FMT3) LOCCTR += 3;
            else if (line.fmt == FMT4) LOCCTR += 4;
            else {
                if (strcmp(line.op, "WORD") == 0)      LOCCTR += 3;
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

    printf("\nProgram length : %06X\n", LOCCTR - start_address);

    for (int i = 0; i < symbol_count; i++) {
        printf("%-10s : %06X\n", SYMTAB[i].symbol, SYMTAB[i].address);
    }

    ASM_close();
    return 0;
}