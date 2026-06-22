"use client"

import * as React from "react"
import { useState } from "react"
import Link from "next/link"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // TODO: Task 9C - Implement Auth Service Integration
    
    setIsSubmitting(false)
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
            <div className="space-y-2">
              <Label htmlFor="email" className="text-white/90">Email</Label>
              <Input 
                id="email" 
                type="email" 
                placeholder="name@example.com" 
                required 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-white/90">Password</Label>
                <Link href="#" className="text-sm font-medium text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input 
                id="password" 
                type="password" 
                required 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
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
                Sign up
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
