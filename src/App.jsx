import { useState, useEffect } from "react";
import { supabase } from "./supabaseClient";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [alumni, setAlumni] = useState([]);

  const handleLogin = async (e) => {
    e.preventDefault();
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) alert("Login Gagal: " + error.message);
    else setUser(data.user);
  };

  useEffect(() => {
    if (user) {
      fetchAlumni();
    }
  }, [user]);

  const fetchAlumni = async () => {
    const { data, error } = await supabase.from("alumni").select("*");
    if (error) {
      console.error("Error fetching:", error.message);
    } else {
      console.log("Data yang didapat:", data);
      setAlumni(data);
    }
  };

  if (user) {
    return (
      <div style={{ padding: "20px", fontFamily: "Arial" }}>
        <h1>Sistem Informasi Alumni (Terproteksi)</h1>
        <button
          onClick={() => supabase.auth.signOut().then(() => setUser(null))}
        >
          Logout
        </button>

        <table
          border="1"
          style={{
            marginTop: "20px",
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr style={{ background: "#eee" }}>
              <th>Nama</th>
              <th>LinkedIn/IG/FB/Tiktok</th>
              <th>Email</th>
              <th>No HP</th>
              <th>Tempat & Alamat Kerja</th>
              <th>Posisi</th>
              <th>Status (PNS/Swasta/Wirausaha)</th>
              <th>Sosmed Kantor</th>
            </tr>
          </thead>
          <tbody>
            {alumni.map((item) => (
              <tr key={item.id}>
                <td>{item.nama_lengkap}</td>
                <td>
                  {item.linkedin || "-"}
                  <br />
                  {item.instagram || "-"}
                  <br />
                  {item.facebook || "-"}
                  <br />
                  {item.tiktok || "-"}
                </td>
                <td>{item.email || "-"}</td>
                <td>{item.no_hp || "-"}</td>
                <td>
                  <strong>{item.tempat_bekerja || "-"}</strong>
                  <br />
                  {item.alamat_bekerja || "-"}
                </td>
                <td>{item.posisi || "-"}</td>
                <td>{item.status_pekerjaan || "-"}</td>
                <td>{item.sosmed_kantor || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Login Admin SPAO</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br />
        <br />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default App;
