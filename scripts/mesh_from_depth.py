# scripts/mesh_from_depth.py
import os
import numpy as np
import open3d as o3d

DEPTH_DIR   = "../assets/depth"
MESH_OUTDIR = "../mesh/from_depth"
os.makedirs(MESH_OUTDIR, exist_ok=True)

# カメラパラメータ例
width, height = 640, 640
intrinsic = o3d.camera.PinholeCameraIntrinsic(
    width, height, fx=1000, fy=1000, cx=width/2, cy=height/2
)

for fname in os.listdir(DEPTH_DIR):
    if not fname.endswith(".npy"): continue
    depth = np.load(os.path.join(DEPTH_DIR, fname))
    # メートル単位に変換（例: depthは正規化済み→仮に1.0mを最大とみなす）
    depth_m = (depth / depth.max()).astype(np.float32)
    depth_img = o3d.geometry.Image((depth_m*1000).astype(np.uint16))

    pcd = o3d.geometry.PointCloud.create_from_depth_image(
        depth_img, intrinsic, extrinsic=np.eye(4)
    )
    pcd.estimate_normals()
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

    out_path = os.path.join(MESH_OUTDIR, fname[:-4] + ".obj")
    o3d.io.write_triangle_mesh(out_path, mesh)
    print(f"Mesh saved: {out_path}")
