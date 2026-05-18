import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)
print("正在啟動互動繪本鏡頭... 請按 'q' 鍵退出。")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. 取得畫面的寬度與高度，用來計算中心點
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # 2. 設定橢圓形的參數 (X軸半徑 120, Y軸半徑 160，大小可依你的鏡頭調整)
    face_oval_axes = (120, 160)
    
    # 預設狀態：白色框線，提示使用者對準
    oval_color = (255, 255, 255)
    current_state = "Please put your face in the circle"
    text_color = (200, 200, 200)

    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion_scores = results[0]['emotion']
        
        # 印出 AI 對你當下表情的真實評分 (這叫打開黑盒子！)
        print(f"開心:{emotion_scores['happy']:5.1f} | 驚訝:{emotion_scores['surprise']:5.1f} | 生氣:{emotion_scores['angry']:5.1f} | 難過:{emotion_scores['sad']:5.1f} | 中性:{emotion_scores['neutral']:5.1f}")
        # 3. 動態回饋：如果情緒達標，改變文字和框框的顏色！
        if emotion_scores['happy'] > 60:
            current_state = "Story Trigger: HAPPY! ^_^"
            text_color = (0, 255, 0)
            oval_color = (0, 255, 0) # 框框變綠色
        elif emotion_scores['sad'] > 60:
            current_state = "Story Trigger: OH NO... (SAD) T_T"
            text_color = (255, 50, 50) # 藍色或紫色
            oval_color = (255, 50, 50)
                    
    except Exception as e:
        pass

    # 4. 把橢圓形畫在畫面上
    # 參數: 畫面, 中心點, 軸長, 旋轉角度, 起始角度, 結束角度, 顏色, 粗細
    cv2.ellipse(frame, (center_x, center_y), face_oval_axes, 0, 0, 360, oval_color, 2)
    
    # 5. 把提示文字放在框框的上方 (座標微調過，讓它盡量置中)
    cv2.putText(frame, current_state, (center_x - 180, center_y - 190), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    cv2.imshow('Interactive Storybook - Magic Mirror', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()