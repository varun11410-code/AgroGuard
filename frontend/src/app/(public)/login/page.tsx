"use client"

import * as React from "react"
import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Eye, EyeOff } from "lucide-react"
import { AuthValidationError } from "@/services/auth"
import { useAuth } from "@/contexts/AuthContext"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

export default function LoginPage() {
  const router = useRouter()
  const { login } = useAuth()
  
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setFieldErrors({})
    setIsSubmitting(true)

    try {
      await login({ email, password })
      router.push("/upload")
    } catch (err: any) {
      if (err instanceof AuthValidationError) {
        const errors: Record<string, string> = {}
        err.errors.forEach(e => {
          errors[e.field] = e.message
        })
        setFieldErrors(errors)
      } else {
        setError(err.message || "Login failed")
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative p-4 z-10 pt-24">
      {/* Aurora Backgrounds from global CSS */}
      <div className="aurora-bg">
        <div className="aurora aurora-1"></div>
        <div className="aurora aurora-2"></div>
        <div className="aurora aurora-3"></div>
      </div>

      {/* Animated Particles */}
      {Array.from({ length: 15 }).map((_, i) => (
        <div
          key={i}
          className="particle"
          style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${10 + Math.random() * 10}s`
          }}
        />
      ))}

      <Card className="w-full max-w-md glass-card-strong relative z-20">
        <CardHeader className="space-y-2 text-center pb-8">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 rounded-xl bg-[linear-gradient(135deg,var(--g),var(--g2))] flex items-center justify-center shadow-[0_0_20px_rgba(34,197,94,0.4)] border border-white/20">
              <span className="text-white font-heading font-bold text-xl">AG</span>
            </div>
          </div>
          <CardTitle className="text-3xl font-bold tracking-tight">Welcome back</CardTitle>
          <CardDescription className="text-muted-foreground/80">
            Enter your credentials to access AgroGuard
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-5">
            {error && (
              <div className="p-3 text-sm font-medium text-destructive-foreground bg-destructive/90 rounded-md">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email" className="text-white/90">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={fieldErrors.email ? "border-red-500" : ""}
              />
              {fieldErrors.email && <p className="text-sm text-red-500 font-medium">{fieldErrors.email}</p>}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-white/90">Password</Label>
                {/*<Link href="#" className="text-sm font-medium text-primary hover:underline">
                  Forgot password?
                </Link>*/}
              </div>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pr-10"
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  onClick={() => setShowPassword(!showPassword)}
                  onMouseDown={(e) => e.preventDefault()}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  aria-pressed={showPassword}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {fieldErrors.password && <p className="text-sm text-red-500 font-medium">{fieldErrors.password}</p>}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4 mt-2">
            <Button
              type="submit"
              className="w-full text-base h-12"
              disabled={isSubmitting}
            >
              Sign In
            </Button>
            <div className="text-center text-sm text-muted-foreground/80">
              Don&apos;t have an account?{" "}
              <Link href="/register" className="font-semibold text-white hover:text-primary transition-colors">
                Create account
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
