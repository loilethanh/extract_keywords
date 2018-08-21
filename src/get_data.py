import csv
from pyvi import ViTokenizer, ViPosTagger
# f = open('names.csv', 'w')
#
# with f:
#     fnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(f, fieldnames=fnames)
#
#     writer.writeheader()
#     writer.writerow({'first_name': 'John', 'last_name': 'Smith'})
#     writer.writerow({'first_name': 'Robert', 'last_name': 'Brown'})
#     writer.writerow({'first_name': 'Julia', 'last_name': 'Griffin'})
st = """Người phụ nữ khiến mỹ nhân Thái Lan phải quỳ gối chính là Sirivannavari Nariratana, công chúa của Hoàng gia Thái Lan, cháu gái Quốc vương Bhumibol Adulyadej. Theo phong tục của người Thái, khi chụp hình chung với công chúa, người dân buộc phải quỳ. 

Công chúa Sirivannavari Nariratana vốn không xa lạ gì với giới thời trang nên hình ảnh các người mẫu, diễn viên nổi tiếng quỳ gối chụp ảnh cùng cô trong các show diễn cũng rất phổ biến."""

st2="Ẩn mình trong khu rừng Vincennes nằm ở phía đông Paris , khu vườn Jardin d ' Agronomie_Tropicale mang những nét kiến_trúc phương Đông kỳ_bí làm không ít người tò_mò . Nhìn bề_ngoài đây giống như một công_viên bị bỏ_hoang nhưng nguồn_gốc của khu vườn này " \
    "hơn 100 năm về trước lại chứa_đựng nhiều điều đen_tối đáng_sợ "
str = ViTokenizer.tokenize(st)
pos = ViPosTagger.postagging(str)
print(str)
print(pos)