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
import type { RegisterFormValues } from "./Register.types";
import { useForm } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { loginCandidate, registerCandidate } from "@/lib/auth";

export default function Register() {
  const [serverSuccessMessage, setServerSuccessMessage] = useState<
    string | null
  >(null);

  const {
    register,
    handleSubmit,
    watch,
    setError,
    clearErrors,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormValues>({
    mode: "onTouched",
    defaultValues: {
      fullName: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const password = watch("password");

  const onSubmit: SubmitHandler<RegisterFormValues> = async (data) => {
    setServerSuccessMessage(null);
    clearErrors("root");

    const res = await registerCandidate(data);

    if (!res.success) {
      setError("root.server", {
        type: "server",
        message: res.message,
      });
      return;
    }
    // console.log(res.data);

    const loginRes = await loginCandidate({
      email: data.email,
      password: data.password,
    });

    if (!loginRes.success) {
      setError("root.server", {
        type: "server",
        message: `Account created, but automatic sign-in failed: ${loginRes.message}`,
      });
      return;
    }

    reset();
    setServerSuccessMessage("Account created and signed in successfully.");
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
            Create account
          </p>
          <h1 className="text-2xl font-semibold tracking-tight text-card-foreground">
            Register
          </h1>
          <p className="text-sm text-muted-foreground">
            Set up your profile to start using Decentrathon.
          </p>
        </header>

        <FieldSet>
          <FieldLegend>Profile</FieldLegend>
          <FieldDescription>
            Use your real details for invoices, account recovery, and email
            notifications.
          </FieldDescription>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="fullName">Full name</FieldLabel>
              <Input
                id="fullName"
                autoComplete="name"
                placeholder="Evelyn Carter"
                aria-invalid={Boolean(errors.fullName)}
                {...register("fullName", {
                  required: "Full name is required.",
                  minLength: {
                    value: 2,
                    message: "Full name must be at least 2 characters.",
                  },
                })}
              />
              <FieldError errors={[errors.fullName]} />
            </Field>

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
          </FieldGroup>
        </FieldSet>

        <FieldSet>
          <FieldLegend>Security</FieldLegend>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input
                id="password"
                autoComplete="new-password"
                type="password"
                aria-invalid={Boolean(errors.password)}
                {...register("password", {
                  required: "Password is required.",
                  minLength: {
                    value: 8,
                    message: "Password must be at least 8 characters.",
                  },
                  pattern: {
                    value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
                    message:
                      "Use at least one uppercase letter, one lowercase letter, and one number.",
                  },
                })}
              />
              <FieldDescription>
                At least 8 characters with uppercase, lowercase, and a number.
              </FieldDescription>
              <FieldError errors={[errors.password]} />
            </Field>

            <Field>
              <FieldLabel htmlFor="confirmPassword">
                Confirm password
              </FieldLabel>
              <Input
                id="confirmPassword"
                autoComplete="new-password"
                type="password"
                aria-invalid={Boolean(errors.confirmPassword)}
                {...register("confirmPassword", {
                  required: "Please confirm your password.",
                  validate: (value) =>
                    value === password || "Passwords do not match.",
                })}
              />
              <FieldError errors={[errors.confirmPassword]} />
            </Field>
          </FieldGroup>
        </FieldSet>

        <div className="flex flex-col gap-3 border-t border-border/60 pt-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-muted-foreground">
            By registering, you agree to the platform terms and privacy policy.
          </p>
          <Button type="submit" size="lg" disabled={isSubmitting}>
            {isSubmitting ? "Creating account..." : "Create account"}
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
