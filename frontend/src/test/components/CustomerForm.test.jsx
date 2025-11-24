import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CustomerForm from '../../components/CustomerForm'

describe('CustomerForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  it('should render form fields', () => {
    render(<CustomerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/phone/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
  })

  it('should call onSubmit with form data when submitted', async () => {
    render(<CustomerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Test Customer' } })
    fireEvent.change(screen.getByLabelText(/location/i), { target: { value: 'Test Location' } })
    fireEvent.change(screen.getByLabelText(/phone/i), { target: { value: '+1234567890' } })
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } })

    fireEvent.click(screen.getByRole('button', { name: /create/i }))

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'Test Customer',
          location: 'Test Location',
          phone: '+1234567890',
          email: 'test@example.com',
        })
      )
    })
  })

  it('should call onCancel when cancel button is clicked', () => {
    render(<CustomerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))

    expect(mockOnCancel).toHaveBeenCalled()
  })
})

