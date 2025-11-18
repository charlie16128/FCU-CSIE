#include <stdio.h>

const char* determine_soldier_type(float height_cm, float weight , float bmi) { //要當什麼兵的判斷
        if (height_cm >= 195) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 32) return "常備役";
        if (bmi >= 32 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 190 && height_cm < 195) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 31.5) return "常備役";
        if (bmi >= 31.5 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 185 && height_cm < 190) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 31) return "常備役";
        if (bmi >= 31 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 180 && height_cm < 185) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 30.5) return "常備役";
        if (bmi >= 30.5 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 175 && height_cm < 180) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 30) return "常備役";
        if (bmi >= 30 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 170 && height_cm < 175) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 29.5) return "常備役";
        if (bmi >= 29.5 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 165 && height_cm < 170) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 29) return "常備役";
        if (bmi >= 29 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 160 && height_cm < 165) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 28.5) return "常備役";
        if (bmi >= 28.5 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else if (height_cm >= 155 && height_cm < 160) {
        if (bmi < 15) return "免役 (因為BMI過低)";
        if (bmi >= 15 && bmi < 16.5) return "免役 (因為BMI過低)";
        if (bmi >= 16.5 && bmi < 28) return "常備役";
        if (bmi >= 28 && bmi < 35) return "替代役";
        if (bmi >= 35) return "免役 (因為BMI過高)";
    }
    else {
        return "免役 (因為身高不符合)";
    }
    return "無法判斷";
}
void bmi(float BMI){  //判斷bmi範圍
    if (BMI < 18.5){
        printf("「體重過輕」，需要多運動，均衡飲食，以增加體能，維持健康\n\n");
    }
    else if(BMI >= 18.5 && BMI < 24){
        printf("恭喜！「健康體重」，要繼續保持！\n\n");
    }
    else if(BMI >= 24 && BMI < 27){
        printf("「體重過重」了，要小心囉，趕快力行「健康體重管理」！\n\n");
    }
    else if (BMI >= 27){
        printf("啊～「肥胖」，需要立刻力行「健康體重管理」囉！\n\n");
    }
}

void bmrprint(float BMR){  //印出bmr建議
    printf("你的BMR為 : %.2f kcal/日\n",BMR);
    printf("身體活動趨於靜態(幾乎不運動)時 : %.2f kcal/日\n",BMR * 1.2);
    printf("身體活動程度較低(每週運動 1-3 天)時 : %.2f kcal/日\n",BMR * 1.375);
    printf("身體活動程度正常(每週運動 3-5 天)時 : %.2f kcal/日\n",BMR * 1.55);
    printf("身體活動程度較高(每週運動 6-7 天)時 : %.2f kcal/日\n",BMR * 1.72);
    printf("身體活動程度激烈(長時間運動或體力勞動工作)時 : %.2f kcal/日\n",BMR * 1.9);
}

int determine_left_eye_degree(float v_left) {  //判斷左眼視力
    if (v_left > 0 && v_left <= 0.1) return 650;
    if (v_left > 0.1 && v_left <= 0.12) return 550;
    if (v_left > 0.12 && v_left <= 0.15) return 500;
    if (v_left > 0.15 && v_left <= 0.2) return 450;
    if (v_left > 0.2 && v_left <= 0.25) return 400;
    if (v_left > 0.25 && v_left <= 0.3) return 350;
    if (v_left > 0.3 && v_left <= 0.4) return 250;
    if (v_left > 0.4 && v_left <= 0.5) return 200;
    if (v_left > 0.5 && v_left <= 0.6) return 150;
    if (v_left > 0.6 && v_left <= 0.8) return 100;
    if (v_left > 0.8) return 0; // 表示視力良好，無近視
    return -1; // 表示無效的視力數據
}

int determine_right_eye_degree(float v_right) {  //判斷右眼視力
    if (v_right > 0 && v_right <= 0.1) return 650;
    if (v_right > 0.1 && v_right <= 0.12) return 550;
    if (v_right > 0.12 && v_right <= 0.15) return 500;
    if (v_right > 0.15 && v_right <= 0.2) return 450;
    if (v_right > 0.2 && v_right <= 0.25) return 400;
    if (v_right > 0.25 && v_right <= 0.3) return 350;
    if (v_right > 0.3 && v_right <= 0.4) return 250;
    if (v_right > 0.4 && v_right <= 0.5) return 200;
    if (v_right > 0.5 && v_right <= 0.6) return 150;
    if (v_right > 0.6 && v_right <= 0.8) return 100;
    if (v_right > 0.8) return 0; // 表示視力良好，無近視
    return -1; // 表示無效的視力數據
}


int main(){
    int weight , age, gender;
    float height_cm , f_height , m_height, vision_left, vision_right;

    printf("請輸入你的\n身高(cm) :");
    scanf("%f",&height_cm);

    printf("體重(kg) :");
    scanf("%d",&weight);

    printf("視力(左) :");
    scanf("%f",&vision_left);

    printf("視力(右) :");
    scanf("%f",&vision_right);

    printf("年齡 :");
    scanf("%d",&age);
    if(age <18){
        printf("請輸入你父親的身高 : ");
        scanf("%f",&f_height);
        printf("請輸入你母親的身高 : ");
        scanf("%f",&m_height);
    }

    printf("性別(男 1、女 0) :");
    scanf("%d", &gender);

    printf("-----\n"); //用以區隔輸入和輸出

    float height = height_cm / 100;         //身高cm換m
    float BMI = weight / (height * height); //計算bmi
    float BMR = 9.99 * weight + 6.25 * height_cm - 4.92 * age + (166 * gender) - 161; //計算基礎代謝量

    printf("\n你的BMI結果為 : %.2f\n\n", BMI);

    bmi(BMI);       //呼叫bmi函式
    bmrprint(BMR);  //呼叫bmrprint函式


    if (gender == 1 && age >= 18){      //18歲以上男生才要當兵
        const char* result = determine_soldier_type(height_cm, weight , BMI);
        printf("\n你要當的兵 : %s\n", result); 
    }
    else if(gender == 1 && age < 18){  //18歲以下男生不用當兵，且輸出未來身高
        printf("\n你還不需要當兵\n"); 
        printf("你成年的身高可能為 : %.2f\n",(f_height + m_height + 13) / 2);
    }
    else if (gender == 0){          //女生不到18 輸出未來身高
        printf("\n女生不需要當兵\n"); 
        printf("你成年的身高可能為 : %.2f\n",(f_height + m_height - 13) / 2);
    }
    else{                           //處理性別不正確!=1 or !=0
        printf("性別錯誤，不等於男生(1)或女生(0)\nError gender = %d\n",gender);
    }

    int left_degree = determine_left_eye_degree(vision_left) , right_degree = determine_right_eye_degree(vision_right); //呼叫函式取得近視度數

    if (left_degree == 0) {
        printf("你的左眼視力良好 : 無近視\n");
    } 
    else if (left_degree == -1) {
        printf("左眼視力數據無效\n");
    } 
    else {
        printf("你的左眼近視度數約為 : %d\n", left_degree);
    }


    if (right_degree == 0) {
        printf("你的右眼視力良好 : 無近視\n");
    } 
    else if (right_degree == -1) {
        printf("右眼視力數據無效\n");
    } 
    else {
        printf("你的右眼近視度數約為 : %d\n", right_degree);
    }

    return 0;   
}