import { Button } from "@/components/ui/button";
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { loginCandidate } from "@/lib/auth";
import { useState } from "react";
import { useForm } from "react-hook-form";

import type { LoginFormValues } from "./Login.types";
import type { SubmitHandler } from "react-hook-form";

export default function Login() {
  const [serverSuccessMessage, setServerSuccessMessage] = useState<
    string | null
  >(null);

  const {
    register,
    handleSubmit,
    setError,
    clearErrors,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    mode: "onTouched",
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit: SubmitHandler<LoginFormValues> = async (data) => {
    setServerSuccessMessage(null);
    clearErrors("root");

    const loginRes = await loginCandidate({
      email: data.email,
      password: data.password,
    });

    if (!loginRes.success) {
      setError("root.server", {
        type: "server",
        message: loginRes.message,
      });
      return;
    }

    setServerSuccessMessage("Signed in successfully. Redirecting...");

    setTimeout(() => {
      window.location.assign("/");
    }, 500);
  };

  return (
    <main className="min-h-screen bg-linear-to-b from-background via-background to-primary/5 px-4 py-10">
      <form
        noValidate
        onSubmit={handleSubmit(onSubmit)}
        className="mx-auto w-full max-w-xl space-y-5 rounded-xl border border-border/70 bg-card p-6 shadow-sm sm:p-8"
      >
        <header className="space-y-2">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-muted-foreground">
            Welcome back
          </p>
          <h1 className="text-2xl font-semibold tracking-tight text-card-foreground">
            Login
          </h1>
          <p className="text-sm text-muted-foreground">
            Sign in with your email and password.
          </p>
        </header>

        <FieldSet>
          <FieldLegend>Account</FieldLegend>
          <FieldDescription>
            Enter the same credentials you used during registration.
          </FieldDescription>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="email">Email</FieldLabel>
              <Input
                id="email"
                autoComplete="email"
                type="email"
                placeholder="you@example.com"
                aria-invalid={Boolean(errors.email)}
                {...register("email", {
                  required: "Email is required.",
                  pattern: {
                    value: /^[\w-.]+@([\w-]+\.)+[\w-]{2,}$/,
                    message: "Enter a valid email address.",
                  },
                })}
              />
              <FieldError errors={[errors.email]} />
            </Field>

            <Field>
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input
                id="password"
                autoComplete="current-password"
                type="password"
                aria-invalid={Boolean(errors.password)}
                {...register("password", {
                  required: "Password is required.",
                })}
              />
              <FieldError errors={[errors.password]} />
            </Field>
          </FieldGroup>
        </FieldSet>

        <div className="flex flex-col gap-3 border-t border-border/60 pt-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-muted-foreground">
            No account yet?{" "}
            <a
              className="text-primary underline underline-offset-2"
              href="/register"
            >
              Create one
            </a>
          </p>
          <Button type="submit" size="lg" disabled={isSubmitting}>
            {isSubmitting ? "Signing in..." : "Sign in"}
          </Button>
        </div>

        {errors.root?.server?.message && (
          <FieldError>{errors.root.server.message}</FieldError>
        )}

        {serverSuccessMessage && (
          <p className="rounded-md border border-primary/25 bg-primary/10 px-3 py-2 text-xs text-primary">
            {serverSuccessMessage}
          </p>
        )}
      </form>
    </main>
  );
}
