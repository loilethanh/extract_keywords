from multi_rake import Rake

text_en = (
    """Clip: Hoa hậu Mỹ Linh lần đầu khoe giọng hát đầy cảm xúc khi song ca cùng Dương Triệu Vũ
Những ai có mặt không giấu nổi sự bất ngờ khi lần đầu nghe Mỹ Linh cất giọng trên sân khấu.
Mới đây, Hoa hậu Mỹ Linh đã có chuyến công tác tại Mỹ và góp mặt trong một đêm nhạc. 
Không chỉ tham gia với tư cách khách mời đặc biệt, người đẹp còn khiến ai nấy bất ngờ khi trổ tài ca hát 
trên sân khấu bằng một tiết mục song ca cùng Dương Triệu Vũ. Đứng cạnh giọng ca "Siêu nhân",
 Mỹ Linh say sưa hát và đắm chìm cảm xúc trong ca khúc "Sau tất cả". Dù không có nhiều kỹ thuật 
 và thật sự xuất sắc nhưng khá đông khán giả nhận xét giọng ca của Mỹ Linh tràn đầy cảm xúc.
"Đây là lần đầu tiên Linh song ca với anh Dương Triệu Vũ. Và cũng là lần đầu tiên, Linh "dám" 
trình diễn trước rất nhiều khán giả. Rất là run và vô cùng may mắn là anh Vũ đã nhường và dìu
 Linh rất nhiều khi hát cùng nhau" - Mỹ Linh thú nhận trong hậu trường. Dù tự nhận bản thân rất thích 
 hát nhưng cô chỉ hát vui và hát vì mối thân tình thôi chứ không dám nhận mình là ca sĩ."""
)

rake = Rake(min_freq=2)

keywords = rake.apply(text_en)

print(keywords[:10])
