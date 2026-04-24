import cv2
import os
import argparse


def extract_frame(video_path, output_path, time_sec=None, frame_index=None):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_index is None:
        if time_sec is None:
            time_sec = 0
        frame_index = int(time_sec * fps)

    if frame_index < 0 or frame_index >= total_frames:
        cap.release()
        raise ValueError(
            f"帧号超出范围: {frame_index}, 视频总帧数: {total_frames}"
        )

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    success, frame = cap.read()
    cap.release()

    if not success:
        raise RuntimeError("读取视频帧失败")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    cv2.imwrite(output_path, frame)

    print(f"已保存单帧图片: {output_path}")
    print(f"FPS: {fps}")
    print(f"提取帧号: {frame_index}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从视频中提取单帧图片")

    parser.add_argument("--video", default=r"C:\Users\DELL\Documents\GitHub\ehnotgod.github.io\pycodes\【哲风壁纸】和服少女-物语花绫.mp4", help="输入视频路径")
    parser.add_argument("--output", default=r"C:\Users\DELL\Documents\GitHub\ehnotgod.github.io\pycodes\frame.jpg", help="输出图片路径")
    parser.add_argument("--time", type=float, default=0.5, help="按时间提取，单位为秒，例如 5.5")
    parser.add_argument("--frame", type=int, help="按帧号提取，例如 120")

    args = parser.parse_args()

    extract_frame(
        video_path=args.video,
        output_path=args.output,
        time_sec=args.time,
        frame_index=args.frame
    )