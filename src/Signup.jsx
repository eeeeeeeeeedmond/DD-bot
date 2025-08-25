import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "./AuthContext"
import showImg from "./assets/visibility_on.png"
import hideImg from "./assets/visibility_off.png"

export default function SignupPage() {
  const [formData, setFormData] = useState({
    userId: "",
    password: "",
    role: "",
  })
  const [showPassword, setShowPassword] = useState(false)

  const [error, setError] = useState("")
  const navigate = useNavigate()
  const { signup, isLoading } = useAuth()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    if (!formData.userId || !formData.password || !formData.role) {
      setError("All fields are required")
      return
    }
    try {
      const result = await signup(formData)
      if (result.success) {
        navigate("/login")
      }
    } catch (err) {
      setError(err.message || "Signup failed")
    }
  }

  return (
    <div className="app">
      <div className="login-container">
        <div className="login-card">
          <h1 className="login-title">Create a New Account</h1>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label className="form-label">User ID</label>
              <input
                type="text"
                name="userId"
                className="form-input"
                value={formData.userId}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group password-group">
            <label className="form-label">Password</label>
            <div className="password-wrapper">
              <input
              type={showPassword ? "text" : "password"}
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required/>
    <img
      src={showPassword ? hideImg : showImg}
      alt="Toggle Password"
      className="toggle-password"
      onClick={() => setShowPassword(!showPassword)}
    />
  </div>
</div>

            <div className="form-group">
              <label className="form-label">Select Role</label>
              <select
                name="role"
                className="form-select"
                value={formData.role}
                onChange={handleChange}
                required
              >
                <option value="">Choose your role...</option>
                <option value="parent">Parent</option>
                <option value="kid">Kid</option>
                <option value="librarian">Librarian</option>
              </select>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" className="login-button" disabled={isLoading}>
              {isLoading ? "Creating..." : "Sign Up"}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
