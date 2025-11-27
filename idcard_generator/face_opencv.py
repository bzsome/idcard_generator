import cv2


def crop_face_opencv(input_img_path, output_img_path):
    # 1. 加载人脸检测模型
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # 模型文件路径
    )

    # 2. 读取图片
    img = cv2.imread(input_img_path)
    if img is None:
        print("错误：无法读取图片")
        return

    # 3. 转为灰度图（人脸检测需灰度图）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. 检测人脸（返回人脸矩形坐标：(x, y, 宽, 高)）
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # 缩放因子（检测不同大小的人脸）
        minNeighbors=5,  # 最小邻域数（过滤误检测）
        minSize=(30, 30)  # 最小人脸尺寸
    )

    if len(faces) == 0:
        print("未检测到人脸")
        return

    # 5. 裁剪第一个检测到的人脸（可循环处理多个人脸）
    x, y, w, h = faces[0]

    # 扩大裁剪范围（避免裁剪到人脸边缘，可选）
    expand_rate = 0.5
    expand = int(w * expand_rate)
    x = max(0, x - expand)
    y = max(0, y - expand)
    w = w + 2 * expand
    h = h + 2 * expand

    # 比例 = 高/宽
    rate_p = 1.333
    h = int(h * rate_p)
    # 上移：增加高度的1/2
    # y = y - int(h * (rate_p - 1) * 0.333)
    face_img = img[y:y + h, x:x + w]  # 矩形裁剪

    # 6. 保存抠图结果
    cv2.imwrite(output_img_path, face_img)
    print(f"人脸抠图完成，保存至：{output_img_path}")


if __name__ == '__main__':
    # 调用函数（替换为你的输入/输出路径）
    crop_face_opencv("input.jpeg", "output_opencv.jpg")
