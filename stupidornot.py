def quiz():
    questions = [
        ("地球是圓的，對嗎？", "Y"),
        ("水能直接從固態變成氣態，對嗎？", "Y"),
        ("太陽從東邊升起，對嗎？", "Y"),
        ("鳥類可以飛行，對嗎？", "Y"),
        ("人類有三隻手指，對嗎？", "N"),
        ("橙子是水果，對嗎？", "Y"),
        ("猴子是哺乳動物，對嗎？", "Y"),
        ("水比油重，對嗎？", "N"),
        ("月亮是一顆星球，對嗎？", "N"),
        ("沙漠中有很多水源，對嗎？", "N")
    ]
    
    correct_answers = 0
    
    for question, correct_answer in questions:
        user_answer = input(question + " (Y/N): ").strip().upper()
        
        if user_answer == correct_answer:
            correct_answers += 1
    
    if correct_answers >= 8:
        print(f"恭喜！你答對了 {correct_answers} 題，算是正常人！")
    else:
        print(f"你答對了 {correct_answers}！是傻瓜!")

quiz()
