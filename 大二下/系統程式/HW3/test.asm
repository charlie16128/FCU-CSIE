COPY    START   0

FIRST   STL     RETARD

        LDB     #LENGTH

        BASE    LENGTH

CLOOP   +JSUB   RDREC

        LDA     LENGTH

        COMP    #0

        JEQ     ENDFIL

        +JSUB   WRREC

        J       CLOOP

ENDFIL  LDA     EOF

        STA     BUFFER

        LDA     #3

        STA     LENGTH

        +JSUB   WRREC

        J       @RETARD

EOF     BYTE    C'EOF'

        RESW    1

        RESW    1

        RESB    4096