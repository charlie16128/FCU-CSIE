MULT9   START   0
MAIN    LDA     #0
        STA     ROW
ROWLOOP LDA     ROW
        COMP    #10
        JEQ     DONE
        LDA     ROW
        COMP    #0
        JEQ     HDRROW
        LDA     ROW
        ADD     ZERO
        JSUB    PCHAR
        J       COLINIT
HDRROW  LDA     SPACE
        JSUB    PCHAR
COLINIT LDA     #1
        STA     COL
COLLOOP LDA     COL
        COMP    #10
        JEQ     ROWEND
        LDA     ROW
        COMP    #0
        JEQ     IHDRCOL
        LDA     ROW
        MUL     COL
        J       DOPRINT
IHDRCOL LDA     COL
DOPRINT JSUB    PRINTA
        LDA     COL
        ADD     #1
        STA     COL
        J       COLLOOP
ROWEND  LDA     NEWLINE
        JSUB    PCHAR
        LDA     NEWLINE
        JSUB    PCHAR
        LDA     ROW
        ADD     #1
        STA     ROW
        J       ROWLOOP
DONE    J       DONE

PRINTA  STA     VALA
        STL     RETPRA
        LDA     VALA
        DIV     TEN
        STA     TENS
        MUL     TEN
        STA     TEMP
        LDA     VALA
        SUB     TEMP
        STA     UNITS
        LDA     SPACE
        JSUB    PCHAR
        LDA     SPACE
        JSUB    PCHAR
        LDA     TENS
        COMP    #0
        JEQ     NOTENS
        ADD     ZERO
        JSUB    PCHAR
        J       PRUNITS
NOTENS  LDA     SPACE
        JSUB    PCHAR
PRUNITS LDA     UNITS
        ADD     ZERO
        JSUB    PCHAR
        LDL     RETPRA
        LDA     VALA
        RSUB

PCHAR   STA     CHAR
PCHLP   TD      OUTDEV
        JEQ     PCHLP
        LDA     CHAR
        WD      OUTDEV
        RSUB

ROW     RESW    1
COL     RESW    1
VALA    RESW    1
RETPRA  RESW    1
TENS    RESW    1
UNITS   RESW    1
TEMP    RESW    1
CHAR    RESW    1
ZERO    WORD    48
SPACE   WORD    32
NEWLINE WORD    10
TEN     WORD    10
OUTDEV  BYTE    X'F2'
        END     MAIN
