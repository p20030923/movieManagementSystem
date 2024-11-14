import json
import sqlite3

def connect_db():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row  # 使查詢結果可以用欄位名稱來存取
    return conn

def mode1_import() -> None:
    """匯入電影資料檔：從 movies.json 檔案匯入電影資料進資料表"""
    try:
        with open('movies.json', 'r', encoding='UTF-8') as f:
        # json.load() 讀取 JSON 檔案，轉換為 Python 的 dict
            data_set = json.load(f)
        # 使用 with 來處理資料庫連接與查詢
        with connect_db() as conn:
            cursor = conn.cursor()
            for data in data_set:
                try:
                    cursor.execute("INSERT INTO movies (title, director, genre, year, rating) VALUES (?, ?, ?, ?, ?)", (data["title"], data["director"],data["genre"],data["year"],data["rating"]))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
            conn.commit()  # 寫入資料
        print("電影已匯入")
    except FileNotFoundError:
        print('找不到檔案...')
    except Exception as e:
        print(f'發生其它錯誤 {e}')

def mode2_check() -> None:
    """查詢電影：可查詢全部電影或特定電影（根據電影名稱）"""
    while True:
        next = input("查詢全部電影嗎？(y/n): ")
        if next == 'y' or next == "Y":
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movies")
                result_all = cursor.fetchall()
                if len(result_all) == 0:
                    print("查無資料")
                    break
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}評分")
                print("-" * 80)
                for data in result_all:
                    print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")
                break
        if next == 'n' or next == "N":
            key = input("請輸入關鍵字: ")
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movies WHERE title like ?", (f'%{key}%',))
                result_all = cursor.fetchall()
                if len(result_all) == 0:
                    print("查無資料")
                    break
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}評分")
                print("-" * 80)
                for data in result_all:
                    print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")
                break
        print("輸入有誤 請重新輸入")

def mode3_add() -> None:
    """新增電影：年份與評分需確保格式正確"""
    title = input("電影名稱: ")
    director = input("導演: ")
    genre = input("類型: ")
    while True:
        try:
        # 執行可能引發異常的程式區塊
            year = int(input("上映年份: "))
        except Exception as e:
            # 處理相應例外的程式碼
            print(f"錯誤訊息為{e}")
            print("請輸入阿拉伯數字")
        else:
            # 當try程式區塊成功執行時，會執行此區塊的程式碼(可省略)
            break
    while True:
        try:
        # 執行可能引發異常的程式區塊
            rating = float(input("評分 (1.0 - 10.0): "))
            if rating < 1 or rating > 10:
                print("評分限輸入 1.0 - 10.0 分")
                continue
        except Exception as e:
            # 處理相應例外的程式碼
            print(f"錯誤訊息為{e}")
            print("請輸入阿拉伯數字")
        else:
            # 當try程式區塊成功執行時，會執行此區塊的程式碼(可省略)
            break
    # 使用 with 來處理資料庫連接與查詢
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO movies (title, director, genre, year, rating) VALUES (?, ?, ?, ?, ?)", (title, director, genre, year, rating))
        except sqlite3.DatabaseError as e:
            print(f"資料庫操作發生錯誤: {e}")
        except Exception as e:
            print(f'發生其它錯誤 {e}')
        conn.commit()  # 寫入資料
    print("電影已新增")

def mode4_edit() -> None:
    """修改電影：若欄位沒有輸入新值代表維持原內容（根據電影名稱）"""
    while True:
        key = input("請輸入要修改的電影名稱: ")
        # 使用 with 來處理資料庫連接與查詢
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies WHERE title = ?", (key,))
            result_all = cursor.fetchall()
            if len(result_all) == 0:
                print("查無資料")
                break
            print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}評分")
            print("-" * 80)
            for data in result_all:
                print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")
        title = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ")
        director = input("請輸入新的導演 (若不修改請直接按 Enter): ")
        genre = input("請輸入新的類型 (若不修改請直接按 Enter): ")
        while True:
            year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ")
            try:
            # 執行可能引發異常的程式區塊
                year = int(year)
            except Exception as e:
                # 處理相應例外的程式碼
                if year == "":
                    break
                else:
                    print(f"錯誤訊息為{e}")
                    print("請輸入阿拉伯數字")
                    continue
            else:
                # 當try程式區塊成功執行時，會執行此區塊的程式碼(可省略)
                break
        while True:
            rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ")
            try:
            # 執行可能引發異常的程式區塊
                rating = float(rating)
                if rating < 1 or rating > 10:
                    print("評分限輸入 1.0 - 10.0 分")
            except Exception as e:
                # 處理相應例外的程式碼
                if rating == "":
                    break
                else:
                    print(f"錯誤訊息為{e}")
                    print("請輸入阿拉伯數字")
                    continue
            else:
                # 當try程式區塊成功執行時，會執行此區塊的程式碼(可省略)
                break
        if title != "": # 判斷有無輸入
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE movies SET title = ? WHERE title = ?', (title, key))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
                conn.commit()  # 寫入資料
        if title != key:
            key = title
        if director != "": # 判斷有無輸入
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE movies SET director = ? WHERE title = ?', (director, key))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
                conn.commit()  # 寫入資料
        if genre != "": # 判斷有無輸入
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE movies SET genre = ? WHERE title = ?', (genre, key))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
                conn.commit()  # 寫入資料
        if year != "": # 判斷有無輸入
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE movies SET year = ? WHERE title = ?', (year, key))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
                conn.commit()  # 寫入資料
        if rating != "": # 判斷有無輸入
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE movies SET rating = ? WHERE title = ?', (rating, key))
                except sqlite3.DatabaseError as e:
                    print(f"資料庫操作發生錯誤: {e}")
                except Exception as e:
                    print(f'發生其它錯誤 {e}')
                conn.commit()  # 寫入資料
        print("資料已修改")
        break

def mode5_del() -> None:
    """刪除電影：可以選擇刪除全部電影或特定電影（根據電影名稱）"""
    while True:
        next = input("刪除全部電影嗎？(y/n): ")
        if next == 'y' or next == "Y":
            next = input("是否要刪除(y/n): ")
            if next == 'y' or next == "Y":
                # 使用 with 來處理資料庫連接與查詢
                with connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM movies")
                    print("電影已刪除")
                    break
            if next == 'n' or next == "N":
                break
        if next == 'n' or next == "N":
            key = input("請輸入關鍵字: ")
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movies WHERE title like ?", (f'%{key}%',))
                result_all = cursor.fetchall()
                if len(result_all) == 0:
                    print("查無資料")
                    break
                print(f"{'電影名稱':{chr(12288)}<10}{'導演':{chr(12288)}<10}{'類型':{chr(12288)}<10}{'上映年份':{chr(12288)}<8}評分")
                print("-" * 80)
                for data in result_all:
                    print(f"{data['title']:{chr(12288)}<10}{data['director']:{chr(12288)}<10}{data['genre']:{chr(12288)}<10}{data['year']:{chr(12288)}<10}{data['rating']:{chr(12288)}<10}")
                next = input("是否要刪除(y/n): ")
                if next == 'y' or next == "Y":
                    cursor.execute("DELETE FROM movies WHERE title like ?", (f'%{key}%',))
                    print("電影已刪除")
                    break
                if next == 'n' or next == "N":
                    break
        print("輸入有誤 請重新輸入")

def mode6_export() -> None:
    """匯出電影：可以選擇匯出全部電影或特定電影（根據電影名稱），匯出名稱為 exported.json"""
    while True:
        next = input("匯出全部電影嗎？(y/n): ")
        if next == 'y' or next == "Y":
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movies")
                result_all = cursor.fetchall()
                if len(result_all) == 0:
                    print("查無資料")
                    break
                data_set = []
                for data in result_all:
                    data_set.append({"id": data["id"], "title": data["title"], "director": data["director"], "genre": data["genre"], "year": data["year"], "rating": data["rating"]})
                with open('exported.json', 'w', encoding="utf-8") as f:
                    # json.dump() 將 dict 轉成 JSON 格式，寫入 JSON 檔案
                    json.dump(data_set, f, ensure_ascii=False, indent=4)
                print("電影資料已匯出至 exported.json")
                break
        if next == 'n' or next == "N":
            key = input("請輸入要匯出的電影名稱: ")
            # 使用 with 來處理資料庫連接與查詢
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movies WHERE title like ?", (f'%{key}%',))
                result_all = cursor.fetchall()
                if len(result_all) == 0:
                    print("查無資料")
                    break
                data_set = []
                for data in result_all:
                    data_set.append({"id": data["id"], "title": data["title"], "director": data["director"], "genre": data["genre"], "year": data["year"], "rating": data["rating"]})
                with open('exported.json', 'w', encoding="utf-8") as f:
                    # json.dump() 將 dict 轉成 JSON 格式，寫入 JSON 檔案
                    json.dump(data_set, f, ensure_ascii=False, indent=4)
                print("電影資料已匯出至 exported.json")
                break
        print("輸入有誤 請重新輸入")