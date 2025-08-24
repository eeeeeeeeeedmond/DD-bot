"use client"

import { createContext, useContext, useState, useEffect } from "react"

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load user from localStorage on app start
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem("user")
      if (savedUser) {
        setUser(JSON.parse(savedUser))
      }
    } catch (error) {
      console.error("Error loading user from localStorage:", error)
      localStorage.removeItem("user")
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Save user to localStorage whenever user state changes
  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user))
    } else {
      localStorage.removeItem("user")
    }
  }, [user])

  const login = async (credentials) => {
    setIsLoading(true)
    try {
      // Mock authentication - replace with real API call
      const mockUsers = {
        admin: { id: "admin001", password: "admin123", redirect: "/admin" },
        parent: { id: "parent001", password: "parent123", redirect: "/parent-dashboard" },
        kid: { id: "kid001", password: "kid123", redirect: "/chat" },
        librarian: { id: "lib001", password: "lib123", redirect: "/librarian-dashboard" },
      }

      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 1000))

      const mockUser = mockUsers[credentials.role]
      if (mockUser && mockUser.id === credentials.userId && mockUser.password === credentials.password) {
        const userData = {
          role: credentials.role,
          userId: credentials.userId,
          loginTime: new Date().toISOString(),
        }
        setUser(userData)
        return { success: true, redirect: mockUser.redirect }
      } else {
        throw new Error("Invalid credentials")
      }
    } catch (error) {
      throw new Error("Login failed. Please check your credentials.")
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
  }

  const isAuthenticated = () => {
    return !!user
  }

  const hasRole = (role) => {
    return user?.role === role
  }

  const getRedirectPath = () => {
    if (!user) return "/login"

    switch (user.role) {
      case "admin":
        return "/admin"
      case "parent":
        return "/parent-dashboard"
      case "kid":
        return "/chat"
      case "librarian":
        return "/librarian-dashboard"
      default:
        return "/login"
    }
  }

  const value = {
    user,
    isLoading,
    login,
    logout,
    isAuthenticated,
    hasRole,
    getRedirectPath,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
