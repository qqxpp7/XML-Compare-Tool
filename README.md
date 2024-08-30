## 目錄 :bookmark:
- [專案介紹](#專案介紹)
- [使用方法](#使用方法)
- [預先準備](#預先準備)
- [功能介紹](#功能介紹)
- [授權](#授權)

## 專案介紹 :loudspeaker:
* 將大的XML檔案拆分為多個小的XML檔案
* 透過比對找出檔案的前後差異
* 產出詳細EXCEL報告

## 使用方法 
### Code名稱 :computer:
* xml_compare_tool：  主畫面
* Pagel：             搜尋
* Page2：             01 位置設定
* Page3：             02 XML拆分
* Page4：             03 找出差異
* Page5：             04 比對-1/2 選擇範圖
* Page5_2：           04 比對-2/2選擇 Element
* Page6：             Copy 資料
* Page7：             Element 分割

### 預先準備 :pushpin:
請先在電腦裡建立好三個資料夾，裡面包含 Before、After、Final三個資料夾。
* Before 是原本的未拆分xml 檔案，拆分後會在底下生成 before_split資料夾。
* After 是修改後的未拆分xml 檔案，拆分後會在底下生成 after_split資料夾、
* Final 是存放所有執行紀錄與報表的資料夾。

### Final產生資料
#### 資料夾 :file_folder:
* Split_report
> 在02 XML拆分->拆分->所產生的結果，是拆分 Before、After 資料夾的執行紀錄，會紀錄是否有重複名稱。
* Move_file
> 在03找出差異->移動差異檔案->所產生的結果，是beforeSplit 跟after_split 有差異的檔案。
* Different_report
> 在03找出差異->執行->所產生的結果，是比對before_Split 跟 after_split 差異檔案的轨行紀錄
* Fixed_tag_report
> 在04比對->下一頁->執行->所產生的结果，是固定Element 的excel 資料夾。
* Changed_a_tag_report
> 在04比對->下一頁->執行->所產生的結果，是變動單一Element 的 excel 資料夾。
* Changed_tags_report
> 在04比對->下一頁->執行->所產生的結果，是變動複數Element的excel 資料夾。
* Copy_file
> 在Copy 資料->COPY->所產生的结果，會從before_split 跟after_split 複製特定 XML 到此資料夾。

#### 文件 :page_facing_up:
* Compare_file_name.txt
> 在04比對->下載->所產生的結果，是before_split資料夾下的所有檔名。
* Compare_file_tag.txt
> 在04比對->下一頁->下載->所產生的結果，是 before-_split 資料夾下隨機一份檔案內的所有element及它的上一層。
* Copy_file_name.txt
> 在 Copy 資料->下載->所產生的結果，是before_split資料夾下的所有 Xml檔名。

## 功能介紹 :wrench:
### 主要功能
1. 位置設定 :file_folder:
> 允許使用者設定before資料夾、after資料夾，以及輸出結果儲存的位置final資料夾。
2. XML拆分 :scissors:
> 依據指定的Element，將before及after資料夾內的XML文件拆分成多個較小的XML文件。
3. 找出差異 :mag_right:
> 用於比對 before_split和 after_split資料夾中擁有相同檔名的文件數量，找出只存在於一方的XML文件，並將差一檔案移動到指定資料夾，同時生成執行紀錄。
4. 比對 :bookmark_tabs:
> 允許使用者手動上傳想要比對的檔案名稱，並新增要比對的Element，最終會產生三個報表：固定Element報表、變動單一Element報表、變動複數Element報表。

### 其他功能
* 搜尋 :mag:
> 使用者選取指定檔案，並展示其在before_split資料夾與after_split資料夾中的內容。
* Copy資料 :books:
> 使用者上傳指定的檔案名稱，將其從before_split資料夾與after_split資料夾複製到final資料夾下的Copy_file資料夾。
* Element 分割 :page_facing_up:

## 授權 :scroll:
此專案使用 [MIT 授權](LICENSE)。
