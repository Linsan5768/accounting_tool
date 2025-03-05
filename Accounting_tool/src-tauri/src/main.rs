use std::env;
use std::process::{Command, Stdio};
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // **强制设置 PATH 变量**
            env::set_var("PATH", "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin");

            // 获取主窗口
            let main_window = app.get_webview_window("main").unwrap();

            // **确保 Python 和 npm 路径正确**
            let _backend = Command::new("/usr/bin/python3") // 确保使用绝对路径
                .current_dir("/Users/lin/LinZ/Accounting_tool/backend") // Python 后端目录
                .arg("app.py") // Flask/FastAPI 入口文件
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to start backend server");

            let _frontend = Command::new("/usr/local/bin/npm") // 确保 npm 路径正确
                .current_dir("/Users/lin/LinZ/Accounting_tool/web_frontend") // Vue 目录
                .arg("run")
                .arg("serve")
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to start frontend server");

            // **等待前端启动**
            std::thread::sleep(std::time::Duration::from_secs(3));

            // **打开 Vue 前端**
            main_window
                .eval("window.location.replace('http://localhost:8080');")
                .unwrap();

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}