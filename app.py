import lib

mode_msg = """
----- 電影管理系統 -----
1. 匯入電影資料檔
2. 查詢電影
3. 新增電影
4. 修改電影
5. 刪除電影
6. 匯出電影
7. 離開系統
------------------------
"""


# 使用 with 來處理資料庫連接與查詢
with lib.connect_db() as conn:
    cursor = conn.cursor()  # 建立 cursor 物件
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,                         -- 電影編號	主鍵，唯一且不可為 NULL
        title TEXT NOT NULL,                            -- 電影名稱 必須有值
        director TEXT NOT NULL,                         -- 導演 必須有值
        genre TEXT NOT NULL,                            -- 類型 必須有值
        year INTEGER NOT NULL,                          -- 上映年份 必須有值
        rating REAL CHECK(rating >= 1 AND rating <= 10) -- 評分 rating 在 1 到 10 之間
    )""")

while True:
    print(mode_msg)
    try:
    # 執行可能引發異常的程式區塊
        mode = int(input("請選擇操作選項: "))
    except Exception as e:
        # 處理相應例外的程式碼
        print(f"錯誤訊息為{e}")
        print("請輸入阿拉伯數字 1 ~ 7")
    else:
        # 當try程式區塊成功執行時，會執行此區塊的程式碼(可省略)
        if mode == 1:
            lib.mode1_import()
        elif mode == 2:
            lib.mode2_check()
        elif mode == 3:
            lib.mode3_add()
        elif mode == 4:
            lib.mode4_edit()
        elif mode == 5:
            lib.mode5_del()
        elif mode == 6:
            lib.mode6_export()
        elif mode == 7:
            print("系統已退出")
            break
        else:
            print("請輸入阿拉伯數字 1 ~ 7")
            continue
    finally:
        # 無論try程式區塊是否發生異常，都執行finally程式碼區塊的程式碼(可省略)
        pass