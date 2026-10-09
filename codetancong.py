import hashlib                    #Tạo mã băm
import importlib.util             #Nạp file python từ đường dẫn
import itertools                  #Tạo tổ hợp, hoán vị, tích descartes
import os                         #Xử lý đường dẫn, kiểm tra file tồn tại hay k
import re                         #Xử lí regex
import string                     #Xử lý chuỗi, tạo ảng ký tự
import sys                        #Xử lý tham số dòng lệnh, thoát chương trình, kết nối chương trình bên ngoài
import time                       #Đo thười gian thực thi
import unicodedata                #Xử lí unicode, chuyển tiếng việt có dấu thành k dấu

TEN_FILE_HAM_BAM = "hambammodulo.py"
TEN_HAM = "custom_hash_modulo"
KY_TU_DAC_BIET = [
    "!", "@", "#", "$", "%", "&", "*",
]
SO_MANH_TOI_DA = 5
SO_KY_TU_DAC_BIET_CO_THE_CHEN = 2
GIOI_HAN_MAT_KHAU = 30_000_000
# =====================================================================
# NẠP HÀM BĂM MODULO TỪ FILE CỦA ĐỘI A
# =====================================================================
def nap_ham_bam_modulo():
    duong_dan = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEN_FILE_HAM_BAM)            
    if not os.path.exists(duong_dan):
        print(f"\n[LỖI] Không tìm thấy file '{TEN_FILE_HAM_BAM}' cùng thư mục.")
        print("      Lấy file hàm băm Modulo mà Đội A đưa, đặt đúng tên này vào.")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("hambammodulo", duong_dan)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, TEN_HAM):
        print(f"\n[LỖI] File '{TEN_FILE_HAM_BAM}' không có hàm '{TEN_HAM}'.")
        sys.exit(1)
    print(f"[+] Đã nạp hàm '{TEN_HAM}' từ '{TEN_FILE_HAM_BAM}'.")
    return getattr(module, TEN_HAM)
def bam_sha256(mat_khau: str) -> str:
    return hashlib.sha256(mat_khau.encode("utf-8")).hexdigest()
# =====================================================================
# NHẬP DỮ LIỆU TỪ BÀN PHÍM
# =====================================================================
def nhap_ho_so() -> dict:
    print("\n--- NHẬP HỒ SƠ MỤC TIÊU ---")
    cac_truong = {
        "ten": "Tên", "ho": "Họ", "nam_sinh": "Năm sinh",
        "ngay_sinh": "Ngày sinh", "thang_sinh": "Tháng sinh",
    }
    ho_so = {}
    for khoa, nhan in cac_truong.items():
        gia_tri = input(f"  {nhan}: ").strip()
        if gia_tri:
            ho_so[khoa] = gia_tri
    if ho_so:
        dem = 1
        while True:
            them = input(f"  Thông tin thêm {dem}: ").strip()
            if not them:
                break
            ho_so[f"thong_tin_them_{dem}"] = them
            dem += 1
    return ho_so
def nhap_so_nguyen(nhan: str) -> int:
    while True:
        try:
            return int(input(f"  {nhan}: ").strip())
        except ValueError:
            print("    -> Nhập số nguyên hợp lệ.")
def nhap_chuoi(nhan: str) -> str:
    while True:
        gia_tri = input(f"  {nhan}: ").strip()
        if gia_tri:
            return gia_tri
        print("    -> Không được để trống.")
def nhap_goi_hash(ten_mat_khau: str) -> dict:
    print(f"\n--- MÃ BĂM CỦA {ten_mat_khau} ---")
    return {
        "hash_modulo": nhap_so_nguyen("Giá trị hash Modulo"),
        "hash_sha256": nhap_chuoi("Chuỗi hash SHA-256"),
    }
# =====================================================================
# SINH ỨNG VIÊN TỪ HỒ SƠ
# =====================================================================
def bo_dau_tieng_viet(chuoi: str) -> str:
    chuoi = chuoi.replace("đ", "d").replace("Đ", "D")
    chuoi_chuan_hoa = unicodedata.normalize("NFD", chuoi)
    chuoi_khong_dau = "".join(
        ky_tu for ky_tu in chuoi_chuan_hoa if unicodedata.category(ky_tu) != "Mn"
    )
    return chuoi_khong_dau
def bien_the_chu_dau_hoa(chuoi: str) -> set:
    if not chuoi:
        return {chuoi}
    return {chuoi.lower(), chuoi.capitalize()}
def bien_the_so_bo_so_0(chuoi_so: str) -> set:
    if not chuoi_so:
        return {""}
    bien_the = {chuoi_so}
    if chuoi_so.isdigit() and chuoi_so.startswith("0") and len(chuoi_so) > 1:
        bien_the.add(str(int(chuoi_so)))
    return bien_the
def bam_nho_ho_so(ho_so: dict) -> list:
    manh = set()
    for gia_tri_goc in ho_so.values():
        gia_tri_khong_dau = bo_dau_tieng_viet(gia_tri_goc)
        for bien_the in bien_the_chu_dau_hoa(gia_tri_khong_dau):
            manh.add(bien_the)
            if " " in bien_the:
                manh.add(bien_the.replace(" ", ""))
                for tu in bien_the.split():
                    manh.add(tu)
            if bien_the.isdigit() and len(bien_the) >= 4:
                manh.add(bien_the[:2])
                manh.add(bien_the[2:])
                manh.add(bien_the[-2:])
        for bien_the_bo_0 in bien_the_so_bo_so_0(gia_tri_khong_dau):
            manh.add(bien_the_bo_0)
    ngay_bien_the = bien_the_so_bo_so_0(ho_so.get("ngay_sinh", ""))
    thang_bien_the = bien_the_so_bo_so_0(ho_so.get("thang_sinh", ""))
    nam_bien_the = bien_the_so_bo_so_0(ho_so.get("nam_sinh", ""))
    for ngay, thang, nam in itertools.product(ngay_bien_the, thang_bien_the, nam_bien_the):
        for a, b in itertools.permutations([ngay, thang, nam], 2):
            if a and b:
                manh.add(a + b)
        for a, b, c in itertools.permutations([ngay, thang, nam], 3):
            if a and b and c:
                manh.add(a + b + c)
    manh.discard("")
    return list(manh)
def sinh_ung_vien(manh_ghep: list, ky_tu_dac_biet: list,
                   so_manh_toi_da: int = SO_MANH_TOI_DA,
                   so_ky_tu_dac_biet_co_the_chen: int = SO_KY_TU_DAC_BIET_CO_THE_CHEN):
    for do_dai in range(1, so_manh_toi_da + 1):
        for to_hop in itertools.permutations(manh_ghep, do_dai):
            goc = "".join(to_hop)
            yield goc
            so_ranh_gioi = do_dai + 1  
            for kt in ky_tu_dac_biet:
                for vi_tri in range(so_ranh_gioi):
                    phan_truoc = "".join(to_hop[:vi_tri])
                    phan_sau = "".join(to_hop[vi_tri:])
                    yield phan_truoc + kt + phan_sau
            if so_ky_tu_dac_biet_co_the_chen >= 2 and so_ranh_gioi >= 2:
                for vi_tri1, vi_tri2 in itertools.combinations(range(so_ranh_gioi), 2):
                    phan1 = "".join(to_hop[:vi_tri1])
                    phan2 = "".join(to_hop[vi_tri1:vi_tri2])
                    phan3 = "".join(to_hop[vi_tri2:])
                    for kt1 in ky_tu_dac_biet:
                        for kt2 in ky_tu_dac_biet:
                            yield phan1 + kt1 + phan2 + kt2 + phan3
def sinh_vet_can(do_dai: int, bang_ky_tu: str):
    for combo in itertools.product(bang_ky_tu, repeat=do_dai):
        yield "".join(combo)
# =====================================================================
# BẺ KHÓA 2 GIAI ĐOẠN: MODULO (lọc nhanh) -> SHA-256 (xác nhận)
# =====================================================================
def be_khoa(danh_sach_ung_vien, ham_modulo, hash_modulo_dich, hash_sha256_dich,
            bao_cao_moi=200_000):
    so_thu = 0
    so_lot = 0
    bat_dau = time.perf_counter()
    for ung_vien in danh_sach_ung_vien:
        so_thu += 1
        if so_thu % bao_cao_moi == 0:
            print(f"    ... đã thử {so_thu:,} mật khẩu")
        if ham_modulo(ung_vien) != hash_modulo_dich:
            continue
        so_lot += 1
        if bam_sha256(ung_vien) == hash_sha256_dich:
            return {
                "thanh_cong": True, "mat_khau": ung_vien,
                "so_thu": so_thu, "so_lot": so_lot,
                "thoi_gian": time.perf_counter() - bat_dau,
            }
    return {
        "thanh_cong": False, "mat_khau": None,
        "so_thu": so_thu, "so_lot": so_lot,
        "thoi_gian": time.perf_counter() - bat_dau,
    }
def in_ket_qua(ten: str, kq: dict):
    print(f"\n--- BÁO CÁO: {ten} ---")
    if kq["thanh_cong"]:
        print(f"[+] BẺ KHÓA THÀNH CÔNG: '{kq['mat_khau']}'")
    else:
        print("[-] Không tìm thấy trong không gian đã thử.")
    print(f"    Số mật khẩu đã thử : {kq['so_thu']:,}")
    print(f"    Số lượt lọt Modulo : {kq['so_lot']:,}")
    print(f"    Thời gian          : {kq['thoi_gian']:.6f} giây")
# =====================================================================
# NHÁNH A: GIẢI MẬT KHẨU 1 (DỰA TRÊN HỒ SƠ)
# =====================================================================
def chay_giai_mat_khau_ho_so(ho_so: dict, ham_modulo):
    mk1 = nhap_goi_hash("MẬT KHẨU 1 (dựa trên hồ sơ)")
    print("\n" + "=" * 70)
    print("YÊU CẦU 1: BỘ SINH TỪ KHÓA (PERMUTATION ENGINE)")
    print("=" * 70)
    manh_ghep = bam_nho_ho_so(ho_so)
    print(f"[*] Đã tạo {len(manh_ghep)} mảnh ghép hồ sơ (không dấu).")
    print(f"[*] Ghép tối đa {SO_MANH_TOI_DA} mảnh/lần, "
          f"chèn tối đa {SO_KY_TU_DAC_BIET_CO_THE_CHEN} ký tự đặc biệt.")
    print(f"[*] Giới hạn an toàn: thử tối đa {GIOI_HAN_MAT_KHAU:,} mật khẩu ")
    nguon_ung_vien = itertools.islice(
        sinh_ung_vien(manh_ghep, KY_TU_DAC_BIET),
        GIOI_HAN_MAT_KHAU,
    )
    print("\n" + "=" * 70)
    print("YÊU CẦU 2: THỬ NGHIỆM BẺ KHÓA MẬT KHẨU HỒ SƠ")
    print("=" * 70)
    kq1 = be_khoa(nguon_ung_vien, ham_modulo, mk1["hash_modulo"], mk1["hash_sha256"])
    in_ket_qua("Mật khẩu 1 - Dựa trên hồ sơ", kq1)
    if not kq1["thanh_cong"] and kq1["so_thu"] >= GIOI_HAN_MAT_KHAU:
        print(f"\n[!] Đã chạm giới hạn {GIOI_HAN_MAT_KHAU:,} mật khẩu mà chưa tìm ra.")
        print("[!] Có thể tăng GIOI_HAN_MAT_KHAU ở đầu file để thử nhiều hơn "
              "(tốn thêm thời gian), hoặc giảm SO_MANH_TOI_DA / "
              "SO_KY_TU_DAC_BIET_CO_THE_CHEN nếu máy chạy quá chậm.")
# =====================================================================
# NHÁNH B: GIẢI MẬT KHẨU 2 (NGẪU NHIÊN)
# =====================================================================
def chay_giai_mat_khau_ngau_nhien(ham_modulo):
    mk2 = nhap_goi_hash("MẬT KHẨU 2 (ngẫu nhiên)")
    do_dai_mk2 = nhap_so_nguyen("Độ dài Mật khẩu 2")
    print("\n" + "=" * 70)
    print("YÊU CẦU 3: THỬ NGHIỆM BẺ KHÓA MẬT KHẨU NGẪU NHIÊN")
    print("=" * 70)
    bang_ky_tu = string.ascii_letters + string.digits + "".join(KY_TU_DAC_BIET)
    khong_gian = len(bang_ky_tu) ** do_dai_mk2
    print(f"[*] Không gian tìm kiếm: {len(bang_ky_tu)}^{do_dai_mk2} = {khong_gian:.3e}")
    GIOI_HAN = 2_000_000
    nguon = itertools.islice(sinh_vet_can(do_dai_mk2, bang_ky_tu), GIOI_HAN)
    kq2 = be_khoa(nguon, ham_modulo, mk2["hash_modulo"], mk2["hash_sha256"], bao_cao_moi=500_000)
    in_ket_qua(f"Mật khẩu 2 - Ngẫu nhiên (giới hạn {GIOI_HAN:,} lượt)", kq2)
    if not kq2["thanh_cong"]:
        ty_le = GIOI_HAN / khong_gian * 100
        toc_do_thu = GIOI_HAN / kq2["thoi_gian"]
        thoi_gian_can = khong_gian / toc_do_thu
        print(f"\n[!] Mới bao phủ {ty_le:.10f}% không gian tìm kiếm.")
        print(f"[!] Ước tính cần ~{thoi_gian_can:.3e}s (~{thoi_gian_can / 3.154e7:.3e} năm) để vét cạn.")
# =====================================================================
# CHƯƠNG TRÌNH CHÍNH
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("ĐỘI B - BÊN TẤN CÔNG")
    print("=" * 70)
    ham_modulo = nap_ham_bam_modulo()
    ho_so = nhap_ho_so()

    if ho_so:
        print(f"\n[+] Đã nhận hồ sơ -> chạy giải MẬT KHẨU HỒ SƠ.")
        chay_giai_mat_khau_ho_so(ho_so, ham_modulo)
    else:
        print(f"\n[+] Không có hồ sơ -> chạy giải MẬT KHẨU NGẪU NHIÊN.")
        chay_giai_mat_khau_ngau_nhien(ham_modulo)
    print("\n" + "=" * 70)
    print("HOÀN TẤT")
    print("=" * 70)