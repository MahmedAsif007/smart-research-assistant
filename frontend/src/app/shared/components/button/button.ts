import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [],
  templateUrl: './button.html',
  styleUrl: './button.scss'
})
export class Button {
  
  clicked = output<void>();

  label = input('Button');

  loading = input(false);

  disabled = input(false);

  variant = input<'primary' | 'secondary'>(
    'primary'
  );
}
