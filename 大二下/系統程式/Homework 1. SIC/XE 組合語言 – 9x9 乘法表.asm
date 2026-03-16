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


——————————



MULT9   START   0       ; 程式開始，起始位址為 0
MAIN    LDA     #0      ; 將暫存器 A 設為 0 (準備初始化列索引)
        STA     ROW     ; 將 0 存入 ROW 變數
ROWLOOP LDA     ROW     ; 載入目前列數
        COMP    #10     ; 比較列數是否達到 10
        JEQ     DONE    ; 若 ROW = 10 則結束程式
        LDA     ROW     ; 載入目前列數以判斷是否為標頭
        COMP    #0      ; 檢查是否為第 0 列 (標頭列)
        JEQ     HDRROW  ; 若是第 0 列，跳轉至 HDRROW
        LDA     ROW     ; 載入 ROW 值準備列印
        ADD     ZERO    ; 加 48 轉換為 ASCII 數字
        JSUB    PCHAR   ; 呼叫 PCHAR 印出列首數字
        J       COLINIT ; 跳轉至欄初始化
HDRROW  LDA     SPACE   ; 載入空白字元
        JSUB    PCHAR   ; 在左上角印出一個空白
COLINIT LDA     #1      ; 將暫存器 A 設為 1 (欄從 1 開始)
        STA     COL     ; 將 1 存入 COL 變數
COLLOOP LDA     COL     ; 載入目前欄數
        COMP    #10     ; 比較欄數是否達到 10
        JEQ     ROWEND  ; 若 COL = 10 則此列結束，跳至 ROWEND
        LDA     ROW     ; 載入列數
        COMP    #0      ; 檢查是否在印標頭列
        JEQ     IHDRCOL ; 若 ROW = 0，直接印出 COL 值
        LDA     ROW     ; 載入列數
        MUL     COL     ; 計算 A = ROW * COL
        J       DOPRINT ; 跳轉至列印邏輯
IHDRCOL LDA     COL     ; 標頭列的值即為 COL
DOPRINT JSUB    PRINTA  ; 呼叫 PRINTA 副程式印出對齊的數字
        LDA     COL     ; 載入目前欄數
        ADD     #1      ; 欄數加 1
        STA     COL     ; 存回 COL
        J       COLLOOP ; 回到內迴圈開頭
ROWEND  LDA     NEWLINE ; 載入換行字元
        JSUB    PCHAR   ; 執行換行
        LDA     NEWLINE ; 再次載入換行字元
        JSUB    PCHAR   ; 執行第二次換行 (符合範例空行)
        LDA     ROW     ; 載入列數
        ADD     #1      ; 列數加 1
        STA     ROW     ; 存回 ROW
        J       ROWLOOP ; 回到外迴圈開頭
DONE    J       DONE    ; 程式結束，無窮迴圈停駐

PRINTA  STA     VALA    ; [副程式] 儲存要印的數值
        STL     RETPRA  ; 儲存回傳位址
        LDA     VALA    ; 載入數值進行除法
        DIV     TEN     ; A = VALA / 10 (取得十位數)
        STA     TENS    ; 儲存十位數
        MUL     TEN     ; 十位數乘 10
        STA     TEMP    ; 暫存十位數之量值
        LDA     VALA    ; 再次載入原數值
        SUB     TEMP    ; 原數 - (十位*10) = 個位數
        STA     UNITS   ; 儲存個位數
        LDA     SPACE   ; 載入空白
        JSUB    PCHAR   ; 印出第 1 個對齊空白
        LDA     SPACE   ; 載入空白
        JSUB    PCHAR   ; 印出第 2 個對齊空白
        LDA     TENS    ; 檢查十位數
        COMP    #0      ; 是否為 0
        JEQ     NOTENS  ; 若為 0，不印數字改印空白
        ADD     ZERO    ; 轉為 ASCII
        JSUB    PCHAR   ; 印出十位數字
        J       PRUNITS ; 跳至印個位數
NOTENS  LDA     SPACE   ; 載入空白
        JSUB    PCHAR   ; 印出空白替代十位數 0
PRUNITS LDA     UNITS   ; 載入個位數
        ADD     ZERO    ; 轉為 ASCII
        JSUB    PCHAR   ; 印出個位數字
        LDL     RETPRA  ; 恢復回傳位址
        LDA     VALA    ; 恢復 A 暫存器原始值
        RSUB            ; 返回主程式

PCHAR   STA     CHAR    ; [副程式] 暫存要印出的字元
PCHLP   TD      OUTDEV  ; 測試裝置 F2 是否準備好
        JEQ     PCHLP   ; 若忙碌則繼續測試
        LDA     CHAR    ; 載入字元
        WD      OUTDEV  ; 寫入裝置 F2
        RSUB            ; 返回

ROW     RESW    1       ; 儲存列計數 (0-9)
COL     RESW    1       ; 儲存欄計數 (1-9)
VALA    RESW    1       ; 副程式暫存 A 值
RETPRA  RESW    1       ; 副程式暫存 L 值
TENS    RESW    1       ; 儲存商數 (十位)
UNITS   RESW    1       ; 儲存餘數 (個位)
TEMP    RESW    1       ; 運算暫存空間
CHAR    RESW    1       ; 字元輸出暫存
ZERO    WORD    48      ; 字元 '0' 的 ASCII 碼
SPACE   WORD    32      ; 空白鍵 的 ASCII 碼
NEWLINE WORD    10      ; 換行符 (LF) 的 ASCII 碼
TEN     WORD    10      ; 常數 10 (用於除法計算)
OUTDEV  BYTE    X'F2'   ; 指定輸出裝置為 F2
        END     MAIN    ; 程式結束

