import pygame, math, random

# 1. 게임 초기화
pygame.init()
# 2. 게임창 옵션 설정
size = [500,900] # 창의 크기를 설정합니다
screen = pygame.display.set_mode(size) # 창 객체를 생성합니다
pygame.display.set_caption("HANGMAN") # 창의 제목을 생성합니다
# 3. 게임 내 필요한 설정
clock = pygame.time.Clock() # 게임 안의 시계를 설정합니다.
# 색상 설정 (검은색, 흰색, 빨간색)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
# 다양한 곳에 사용될 폰트 설정
hint_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 80)
entry_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 60)
no_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 40)
title_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 80)
guide_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 20)
finish_font = pygame.font.Font("/Library/Fonts/Arial Unicode.ttf", 30)
# 다양한 곳에 사용될 소리 저장
sound_bad = pygame.mixer.Sound("bad.ogg")
sound_good = pygame.mixer.Sound("good.ogg")
sound_clock = pygame.mixer.Sound("clock.ogg")
sound_save = pygame.mixer.Sound("save.ogg")
sound_fail = pygame.mixer.Sound("fail.ogg")
# 소리 볼륨 조절
sound_bad.set_volume(0.2)
sound_good.set_volume(0.2)
sound_clock.set_volume(0.2)
sound_save.set_volume(0.2)
sound_fail.set_volume(0.2)

# 튜플을 매개변수로 받아 각 요소를 반올림하여 다시 변환합니다
def tup_r(tup):
    temp_list = []
    
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

exit = False
while not exit: # 게임이 종료되지 않는 동안 반복
    entry_text = ""
    drop = False
    enter_go = False
    ready = False
    game_over = False
    save = False
    play_again = False

    #  A가 영어 단어를 1개 생각한다.
    f = open("voca.txt","r",encoding='UTF-8')
    raw_data = f.read() # 단어 리스트가 저장된 파일을 읽습니다.
    f.close()
    data_list = raw_data.split("\n") # 엔터를 기준으로 데이터를 분리
    data_list = data_list[:-1] # 마지막에 \n을 제거합니다.
    while True:
        r_index = random.randrange(0,len(data_list)) # 단어를 랜덤으로 지정할 인덱스
        word = data_list[r_index].replace(u"\xa0", u" ").split(" ")[1] # 단어 지정
        if len(word) <= 6 :break # 6자 이하일 경우에 반복문 종료
    word = word.upper() # 해당 단어를 대문자로 변환
    
    #  단어의 글자 수만큼 밑줄을 긋는다.
    word_show = "_"*len(word)
    try_num = 0 # 시도 횟수
    ok_list = [] # 맞춘 글자 리스트
    no_list = [] # 오답 글자 리스트

    k = 0
    # 시작 화면
    sound_save.stop()
    sound_fail.stop()
    while not exit:
        clock.tick(60) # 초당 프레임 설정
        for event in pygame.event.get(): # 이벤트 처리 반복문
            if event.type == pygame.QUIT: # 창 닫았을 경우 
                exit = True # 종료
            if event.type == pygame.KEYDOWN: # 키 눌렸을 경우
                ready = True # 준비 완료
        if ready == True: break # 준비 완료이면 반복문 종료        
        screen.fill(black) # 검은색 화면 준비
        title = title_font.render("HANGMAN", True, white) # 제목 표시
        title_size = title.get_size()
        title_pos = tup_r((size[0]/2-title_size[0]/2, size[1]/2-title_size[1]/2))
        screen.blit(title, title_pos)
        # 안내문 표시
        guide = guide_font.render("PRESS ANY KEY TO START THE GAME", True, white)
        guide_size = guide.get_size()
        guide_pos = tup_r((size[0]/2-guide_size[0]/2, size[1]*4/5-guide_size[1]/2))
        # 초마다 안내문이 깜빡
        if pygame.time.get_ticks() % 1000 > 500 :
            screen.blit(guide, guide_pos)    
        pygame.display.flip()
        
    # 4. 메인 이벤트
    sound_clock.play(-1) # 효과음 반복
    while not exit:
        # 4-1. FPS 설정
        clock.tick(60) # 초당 60프레임 설정
        # 4-2. 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True # 창 닫으면 종료
            if event.type == pygame.KEYDOWN:
                if drop == False and try_num == 8: # 빨간줄이 길어지는 동안
                    continue # 키 입력을 무시
                # 게임 종료되었을 시 다시 플레이 여부 질문
                if game_over == True: play_again = True
                key_name = pygame.key.name(event.key)
                # 엔터키 눌렸을 경우
                if (key_name == "return" or key_name == "enter"):
                    # 입력한 문자열이 비어있지 않고 입력했던 이력이 있는 문자열이 아닐 경우
                    if entry_text != "" and (ok_list+no_list).count(entry_text) == 0 :
                        enter_go = True # 완료 표시           
                # 알파벳 키가 눌렸을 경우
                elif len(key_name) == 1:
                    # 대문자로 변환하여 입력창에 표시
                    if (ord(key_name) >= 65 and ord(key_name) <= 90) or (ord(key_name) >= 97 and ord(key_name) <= 122):
                        entry_text = key_name.upper()
                    else : entry_text = "" # 알파벳이 아닐 경우
                else : entry_text = "" # 특수문자

        # 4-3. 입력, 시간에 따른 변화
        if play_again == True : break # 다시 플레이 할 경우 반복문 탈출
        if try_num == 8 : k += 1 # 빨간줄 표시
        if enter_go == True: # 사용자 입력 완료일 경우
            ans = entry_text # 입력된 글자를 저장
            result = word.find(ans) # 입력된 글자가 정답에 포함되어있는지 판단
            if result == -1 : # 없을 경우
                try_num += 1 # 시도 횟수 1증가
                no_list.append(ans) # 오답 리스트에 추가
                sound_bad.play()
            else : #있음
                ok_list.append(ans) # 정답 리스트에 추가
                # 정답 단어 표시할 문자열 업데이트
                for i in range(len(word)):
                    if word[i] == ans:
                        word_show = word_show[:i] + ans + word_show[i+1:]
                sound_good.play()
            enter_go = False # 입력 처리 완료이므로 다시 원상복구
            entry_text = ""
        if drop == True: # 실패로 종료
            game_over = True # 게임 종료
            word_show = word # 정답 공개
            sound_clock.stop()
            
        if word_show.find("_") == -1 and game_over == False : # 성공으로 종료
            game_over = True # 게임 종료
            save = True # 사람 생존
            sound_clock.stop() 
            sound_save.play()
        # 4-4. 그리기
        screen.fill(black) # 화면을 검은색으로 채움
        A = tup_r((0, size[1]*2/3)) # 첫 번째 수평선의 시작점
        B = (size[0], A[1]) # 첫 번째 수평선의 끝점
        C = tup_r((size[0]/6 , A[1])) # 첫 번째 수직선의 시작점
        D = (C[0], C[0]) # 첫 번째 수직선의 끝점
        E = tup_r((size[0]/2, D[1])) # 두 번째 수직선의 시작점
        # 기둥과 교차선을 그림
        if save != True:
            pygame.draw.line(screen, white, A, B, 3)
            pygame.draw.line(screen, white, C, D, 3)
            pygame.draw.line(screen, white, D, E, 3)
        F = tup_r((E[0], E[1]+size[0]/6))
        if drop == False and save != True:
            pygame.draw.line(screen, white, E, F, 3)
        r_head = round(size[0]/12)
        # 실패한 경우 머리를 그린다
        if drop == True : G = (F[0],F[1]+r_head+k*10)
        else : G = (F[0],F[1]+r_head)
        # 시도 횟수가 1이상이거나 정답일 경우 머리를 그린다
        if try_num >= 1 or save == True: pygame.draw.circle(screen, white, G, r_head, 3)
        H = (G[0], G[1]+r_head)
        I = (H[0], H[1]+r_head)
        # 시도 횟수가 2 이상이서나 정답일 경우 목을 그린다
        if try_num >= 2 or save == True:pygame.draw.line(screen, white, H, I, 3)
        # 팔의 위치 정보
        l_arm = r_head*2
        J = (I[0]-l_arm*math.cos(30*math.pi/180),
            I[1]+l_arm*math.sin(30*math.pi/180))
        K = (I[0]+l_arm*math.cos(30*math.pi/180),
            I[1]+l_arm*math.sin(30*math.pi/180))
        J = tup_r(J)
        K = tup_r(K)
        # 시도 횟수가 3 이상이거나 정답일 경우 왼쪽 팔을 그린다 
        if try_num >= 3 or save == True:pygame.draw.line(screen, white, I, J, 3)
        # 시도 횟수가 3 이상이거나 정답일 경우 오른쪽 팔을 그린다 
        if try_num >= 4 or save == True:pygame.draw.line(screen, white, I, K, 3)
        L = (I[0], I[1]+l_arm)
        # 시도 횟수가 5 이상이거나 정답일 경우 몸통을 그린다 
        if try_num >= 5 or save == True:pygame.draw.line(screen, white, I, L, 3)
        # 다리 위치 정보
        l_leg = round(l_arm * 1.5)
        M = (L[0]-l_leg*math.cos(60*math.pi/180),
            L[1]+l_leg*math.sin(60*math.pi/180))
        N = (L[0]+l_leg*math.cos(60*math.pi/180),
            L[1]+l_leg*math.sin(60*math.pi/180))  
        M = tup_r(M)
        N = tup_r(N)  
        # 시도 횟수가 6 이상이거나 정답일 경우 왼쪽 다리를 그린다 
        if try_num >= 6 or save == True:pygame.draw.line(screen, white, L, M, 3)
        # 시도 횟수가 7 이상이거나 정답일 경우 오른쪽 다리를 그린다     
        if try_num >= 7 or save == True:pygame.draw.line(screen, white, L, N, 3)  
        # 시도 횟수가 8번일 경우와 아직 실패하지 않았을 경우
        if drop == False and try_num == 8:
            O = tup_r((size[0]/2-size[0]/6, E[1]/2+F[1]/2))
            P = (O[0]+k*2, O[1])
            if P[0] > size[0]/2+size[0]/6 :
                P = tup_r((size[0]/2+size[0]/6, O[1]))
                drop = True
                k = 0
                sound_fail.play()
            # 게임 실패를 기록하고 빨간 줄을 그린다
            pygame.draw.line(screen, red, O, P, 3)
        # 힌트 표시하기
        hint = hint_font.render(word_show, True, white)
        hint_size = hint.get_size()
        hint_pos = tup_r((size[0]/2-hint_size[0]/2, size[1]*5/6-hint_size[1]/2))
        screen.blit(hint, hint_pos)
        # 입력창 표시하기
        entry = entry_font.render(entry_text, True, black)
        entry_size = entry.get_size()
        entry_pos = tup_r((size[0]/2-entry_size[0]/2, size[1]*17/18-entry_size[1]/2))
        entry_bg_size = 80
        pygame.draw.rect(screen, white, tup_r((size[0]/2-entry_bg_size/2, size[1]*17/18-entry_bg_size/2
                                        ,entry_bg_size ,entry_bg_size)))
        screen.blit(entry, entry_pos)
        # 오답 표시하기
        no_text = " ".join(no_list)
        no = no_font.render(no_text, True, red)
        no_pos = tup_r((20, size[1]*2/3+20))
        screen.blit(no, no_pos)
        # 종료 화면
        if game_over == True:
            finish_bg = pygame.Surface(size)
            finish_bg.fill(black)
            finish_bg.set_alpha(200)
            screen.blit(finish_bg, (0,0))
            if save == True: finish_text = "You saved the man"
            else : finish_text = "You killed the man"
            finish = finish_font.render(finish_text, True, white)
            finish_size = finish.get_size()
            finish_pos = tup_r((size[0]/2-finish_size[0]/2, size[1]*3/4-finish_size[1]/2))
            screen.blit(finish, finish_pos)
            guide = guide_font.render("PRESS ANY KEY TO PLAY AGAIN", True, white)
            guide_size = guide.get_size()
            guide_pos = tup_r((size[0]/2-guide_size[0]/2, size[1]*4/5-guide_size[1]/2))
            screen.blit(guide, guide_pos)          
        # 4-5. 업데이트
        pygame.display.flip()
# 5. 게임 종료
pygame.quit()