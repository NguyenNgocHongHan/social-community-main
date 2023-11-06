function refresh() {
    // Sử dụng Fetch API để gửi yêu cầu GET đến máy chủ
    fetch('/get_follower')
    .then(response => response.json())
    .then(data => {
        // Hiển thị thông điệp từ máy chủ trên giao diện
        document.getElementById('group-fb').innerText = data.dataall;
        document.getElementById('fanpage-fb').innerText = data.time;
    })
    .catch(error => console.error('Error:', error));
}