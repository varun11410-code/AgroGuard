import * as React from "react"
import { Loader2 } from "lucide-react"

import { cn } from "@/lib/utils"

export interface LoadingProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "spinner" | "dots" | "pulse"
  size?: "sm" | "md" | "lg"
}

const Loading = React.forwardRef<HTMLDivElement, LoadingProps>(
  ({ className, variant = "spinner", size = "md", ...props }, ref) => {
    return (
      <div
        ref={ref}
        role="status"
        aria-label="Loading"
        className={cn(
          "inline-flex items-center justify-center text-primary",
          variant === "dots" && "gap-1.5",
          className
        )}
        {...props}
      >
        {variant === "spinner" && (
          <Loader2
            className={cn("motion-safe:animate-spin", {
              "w-4 h-4": size === "sm",
              "w-6 h-6": size === "md",
              "w-8 h-8": size === "lg",
            })}
          />
        )}

        {variant === "dots" && (
          <>
            <div
              className={cn(
                "bg-current rounded-full motion-safe:animate-bounce [animation-delay:-0.3s]",
                {
                  "w-1.5 h-1.5": size === "sm",
                  "w-2.5 h-2.5": size === "md",
                  "w-3 h-3": size === "lg",
                }
              )}
            />
            <div
              className={cn(
                "bg-current rounded-full motion-safe:animate-bounce [animation-delay:-0.15s]",
                {
                  "w-1.5 h-1.5": size === "sm",
                  "w-2.5 h-2.5": size === "md",
                  "w-3 h-3": size === "lg",
                }
              )}
            />
            <div
              className={cn("bg-current rounded-full motion-safe:animate-bounce", {
                "w-1.5 h-1.5": size === "sm",
                "w-2.5 h-2.5": size === "md",
                "w-3 h-3": size === "lg",
              })}
            />
          </>
        )}

        {variant === "pulse" && (
          <div
            className={cn("rounded-full bg-current motion-safe:animate-pulse", {
              "w-4 h-4": size === "sm",
              "w-6 h-6": size === "md",
              "w-8 h-8": size === "lg",
            })}
          />
        )}

        <span className="sr-only">Loading...</span>
      </div>
    )
  }
)
Loading.displayName = "Loading"

export { Loading }
